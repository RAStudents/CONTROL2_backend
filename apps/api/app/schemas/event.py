from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class EventMeta(BaseModel):
    id: str
    code: str
    occurred_at: datetime
    started_at: datetime | None = None
    ended_at: datetime | None = None
    duration_ms: int | None = None
    idempotency_key: str
    sequence: int | None = None


class DeviceInfo(BaseModel):
    id: str
    external_id: str | None = None
    hostname: str | None = None


class BindingInfo(BaseModel):
    id: str | None = None


class SourceInfo(BaseModel):
    camera_id: str | None = None
    camera_role: str | None = None
    frame_width: int | None = None
    frame_height: int | None = None
    fps: float | None = None


class ModelInfo(BaseModel):
    name: str | None = None
    version: str | None = None
    config_version: str | None = None
    runtime: str | None = None
    runtime_version: str | None = None
    artifact_sha256: str | None = None


class ClassInfo(BaseModel):
    id: int | None = None
    name: str


class GeometryInfo(BaseModel):
    type: str
    coordinates: list[float]


class DetectionInfo(BaseModel):
    id: str | int | None = None
    class_: ClassInfo = Field(alias="class")
    confidence: float | None = None
    geometry: GeometryInfo


class InferenceInfo(BaseModel):
    task: str
    threshold: float | None = None
    latency_ms: float | None = None
    detections: list[DetectionInfo] = []


class MediaInfo(BaseModel):
    preview: str | None = None
    video: str | None = None


class CpuInfo(BaseModel):
    usage_percent: float | None = None
    temperature_c: float | None = None


class GpuInfo(BaseModel):
    usage_percent: float | None = None
    temperature_c: float | None = None
    memory_usage_percent: float | None = None


class MemoryInfo(BaseModel):
    usage_percent: float | None = None
    used_mb: int | None = None
    total_mb: int | None = None


class StorageInfo(BaseModel):
    usage_percent: float | None = None


class NetworkInfo(BaseModel):
    rssi_dbm: float | None = None
    latency_ms: float | None = None


class DeviceSnapshot(BaseModel):
    captured_at: datetime
    cpu: CpuInfo | None = None
    gpu: GpuInfo | None = None
    memory: MemoryInfo | None = None
    storage: StorageInfo | None = None
    network: NetworkInfo | None = None


class PerformanceInfo(BaseModel):
    capture_latency_ms: float | None = None
    preprocess_latency_ms: float | None = None
    inference_latency_ms: float | None = None
    postprocess_latency_ms: float | None = None
    total_latency_ms: float | None = None
    fps_input: float | None = None
    fps_processed: float | None = None


class EventIn(BaseModel):
    schema_version: str
    event: EventMeta
    device: DeviceInfo
    binding: BindingInfo | None = None
    source: SourceInfo | None = None
    model: ModelInfo | None = None
    inference: InferenceInfo | None = None
    media: MediaInfo | None = None
    device_snapshot: DeviceSnapshot | None = None
    performance: PerformanceInfo | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    received_at: datetime | None = None