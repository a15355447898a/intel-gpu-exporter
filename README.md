# intel-gpu-exporter

> [!NOTE]
> This is a fork of the original `onedr0p/intel-gpu-exporter` which appears to be no longer maintained. This version has been updated to support newer versions of `intel-gpu-tools`.

## Recent Changes
This version includes several key fixes:
- **Updated Metric Parsing**: The script now correctly parses the JSON output from newer versions of `intel_gpu_top` where engine names (e.g., `Render/3D`) do not have a `/0` suffix.
- **Added Compute Metric**: Support for the `Compute` engine has been added.
- **Robust JSON Streaming**: The JSON parsing logic was completely rewritten to be more robust, correctly handling streaming JSON arrays from `intel_gpu_top` to prevent errors.
- **Updated Grafana Dashboard**: The Grafana dashboard JSON has been updated to match the new metric names and includes a panel for the new `Compute` metric.

## Deployment

Runs on port 8080, using python and `intel_gpu_top` to export metrics for Prometheus.

### Docker Compose

To build and run your local, modified version:
```yaml
version: "3.8"

services:
  intel-gpu-exporter:
    build: .
    image: intel-gpu-exporter:custom
    container_name: intel-gpu-exporter
    restart: unless-stopped
    privileged: true
    pid: host
    ports:
      - 8080:8080
    volumes:
      - /dev/dri/:/dev/dri/
```

## Metrics

The following metrics are exposed:

```bash
# HELP igpu_engines_blitter_busy Blitter busy utilisation %
# TYPE igpu_engines_blitter_busy gauge
igpu_engines_blitter_busy 0.0
# HELP igpu_engines_blitter_sema Blitter sema utilisation %
# TYPE igpu_engines_blitter_sema gauge
igpu_engines_blitter_sema 0.0
# HELP igpu_engines_blitter_wait Blitter wait utilisation %
# TYPE igpu_engines_blitter_wait gauge
igpu_engines_blitter_wait 0.0
# HELP igpu_engines_render_3d_busy Render 3D busy utilisation %
# TYPE igpu_engines_render_3d_busy gauge
igpu_engines_render_3d_busy 0.0
# HELP igpu_engines_render_3d_sema Render 3D sema utilisation %
# TYPE igpu_engines_render_3d_sema gauge
igpu_engines_render_3d_sema 0.0
# HELP igpu_engines_render_3d_wait Render 3D wait utilisation %
# TYPE igpu_engines_render_3d_wait gauge
igpu_engines_render_3d_wait 0.0
# HELP igpu_engines_video_busy Video busy utilisation %
# TYPE igpu_engines_video_busy gauge
igpu_engines_video_busy 0.0
# HELP igpu_engines_video_sema Video sema utilisation %
# TYPE igpu_engines_video_sema gauge
igpu_engines_video_sema 0.0
# HELP igpu_engines_video_wait Video wait utilisation %
# TYPE igpu_engines_video_wait gauge
igpu_engines_video_wait 0.0
# HELP igpu_engines_video_enhance_busy Video Enhance busy utilisation %
# TYPE igpu_engines_video_enhance_busy gauge
igpu_engines_video_enhance_busy 0.0
# HELP igpu_engines_video_enhance_sema Video Enhance sema utilisation %
# TYPE igpu_engines_video_enhance_sema gauge
igpu_engines_video_enhance_sema 0.0
# HELP igpu_engines_video_enhance_wait Video Enhance wait utilisation %
# TYPE igpu_engines_video_enhance_wait gauge
igpu_engines_video_enhance_wait 0.0
# HELP igpu_engines_compute_busy Compute busy utilisation %
# TYPE igpu_engines_compute_busy gauge
igpu_engines_compute_busy 0.0
# HELP igpu_engines_compute_sema Compute sema utilisation %
# TYPE igpu_engines_compute_sema gauge
igpu_engines_compute_sema 0.0
# HELP igpu_engines_compute_wait Compute wait utilisation %
# TYPE igpu_engines_compute_wait gauge
igpu_engines_compute_wait 0.0
# HELP igpu_frequency_actual Frequency actual MHz
# TYPE igpu_frequency_actual gauge
igpu_frequency_actual 0.0
# HELP igpu_frequency_requested Frequency requested MHz
# TYPE igpu_frequency_requested gauge
igpu_frequency_requested 0.0
# HELP igpu_imc_bandwidth_reads IMC reads MiB/s
# TYPE igpu_imc_bandwidth_reads gauge
igpu_imc_bandwidth_reads 0.0
# HELP igpu_imc_bandwidth_writes IMC writes MiB/s
# TYPE igpu_imc_bandwidth_writes gauge
igpu_imc_bandwidth_writes 0.0
# HELP igpu_interrupts Interrupts/s
# TYPE igpu_interrupts gauge
igpu_interrupts 0.0
# HELP igpu_period Period ms
# TYPE igpu_period gauge
igpu_period 0.0
# HELP igpu_power_gpu GPU power W
# TYPE igpu_power_gpu gauge
igpu_power_gpu 0.0
# HELP igpu_power_package Package power W
# TYPE igpu_power_package gauge
igpu_power_package 0.0
# HELP igpu_rc6 RC6 %
# TYPE igpu_rc6 gauge
igpu_rc6 0.0
```