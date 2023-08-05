"""Timeseer Client allows querying of data and metadata."""

import json
import time

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

from kukur import Metadata, SeriesSelector
from kukur.client import Client as KukurClient

import pyarrow as pa
import pyarrow.flight as fl


class Client(KukurClient):
    """Client connects to Timeseer using Arrow Flight."""

    def upload_data(self, metadata: Metadata, table: pa.Table):
        """Upload data for one time series to Timeseer and run data quality checks on it.

        This requires a configured 'flight-upload' source in Timeseer.

        Args:
            metadata: any known metadata about the time series. This will be merged with the metadata
                already known by Timeseer depending on the source configuration. The source of the series should match
                the source name of a 'flight-upload' source.
            table: a pyarrow.Table of two columns.
                The first column with name 'ts' contains Arrow timestamps.
                The second column with name 'value' contains the values as a number or string.

        Waits until the analysis is done.
        """
        metadata_json = metadata.to_data()
        metadata_json["series"] = {
            "source": metadata.series.source,
            "name": metadata.series.name,
        }
        descriptor = fl.FlightDescriptor.for_command(json.dumps(metadata_json))
        client = self._get_client()
        writer, reader = client.do_put(descriptor, table.schema)
        writer.write_table(table)
        writer.done_writing()
        buf: pa.Buffer = reader.read()
        response: Dict[str, int] = json.loads(buf.to_pybytes())
        writer.close()

        while True:
            results = list(
                client.do_action(
                    ("get_flow_evaluation_state", json.dumps(response).encode())
                )
            )
            state = json.loads(results[0].body.to_pybytes())
            if (
                state["completed"] == state["total"]
                and state["blockCompleted"] == state["blockTotal"]
            ):
                break
            time.sleep(1)

    def get_event_frames(
        self,
        selector: SeriesSelector,
        start_date: datetime = None,
        end_date: datetime = None,
        frame_type: str = None,
    ) -> pa.Table:
        """Get all event frames matching the given criteria.

        Args:
            selector: the time series source, exposed flow or time series to which the event frames are linked.
            start_date: the start date of the range to find overlapping event frames in. Defaults to one year ago.
            end_date: the end date of the range to find overlapping event frames in. Defaults to now.
            frame_type: the type of event frames to search for. Finds all types when empty.

        Returns::
            A pyarrow Table with 4 columns.
            The first column ('start_date') contains the start date.
            The second column ('end_date') contains the end date.
            The third column ('type') contains the type of the returned event frame as a string.
            Columns 4 contains possible multiple references for the event frame.
        """
        if start_date is None or end_date is None:
            now = datetime.utcnow().replace(tzinfo=timezone(timedelta(0)))
            if start_date is None:
                start_date = now.replace(year=now.year - 1)
            if end_date is None:
                end_date = now

        query: Dict[str, Any] = {
            "query": "get_event_frames",
            "selector": {"source": selector.source},
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        }

        if selector.name is not None:
            query["selector"]["name"] = selector.name

        if frame_type is not None:
            query["type"] = frame_type

        ticket = fl.Ticket(json.dumps(query))
        return self._get_client().do_get(ticket).read_all()

    def get_data_quality_score_data_sources(
        self, source_names: List[str]
    ) -> dict[str, int]:
        """Get the data quality score of a data source or exposed flow.

        Args:
            source_names: A list of time series sources or Flight Expose blocks

        Returns::
            A data quality score of every given source as a percentage.
        """
        body = {
            "source_names": source_names,
        }
        results = list(
            self._get_client().do_action(
                ("get_data_quality_score_data_sources", json.dumps(body).encode())
            )
        )
        return json.loads(results[0].body.to_pybytes())

    def get_kpi_scores(
        self,
        source_name: str,
    ) -> dict[str, dict[str, int]]:
        """Get the kpi scores of a data source or exposed flow.

        Args:
            source_name: The time series source or the name of the Flight Expose block.

        Returns::
            The score per KPI as a percentage, keyed by the source_name provided.
        """
        body = {
            "source_name": source_name,
        }

        results = list(
            self._get_client().do_action(("get_kpi_scores", json.dumps(body).encode()))
        )
        return json.loads(results[0].body.to_pybytes())
