from prometheus_client import start_http_server, Gauge
import os
import sys
import subprocess
import json
import logging

igpu_engines_blitter_busy = Gauge(
    "igpu_engines_blitter_busy", "Blitter busy utilisation %"
)
igpu_engines_blitter_sema = Gauge(
    "igpu_engines_blitter_sema", "Blitter sema utilisation %"
)
igpu_engines_blitter_wait = Gauge(
    "igpu_engines_blitter_wait", "Blitter wait utilisation %"
)

igpu_engines_render_3d_busy = Gauge(
    "igpu_engines_render_3d_busy", "Render 3D busy utilisation %"
)
igpu_engines_render_3d_sema = Gauge(
    "igpu_engines_render_3d_sema", "Render 3D sema utilisation %"
)
igpu_engines_render_3d_wait = Gauge(
    "igpu_engines_render_3d_wait", "Render 3D wait utilisation %"
)

igpu_engines_video_busy = Gauge(
    "igpu_engines_video_busy", "Video busy utilisation %"
)
igpu_engines_video_sema = Gauge(
    "igpu_engines_video_sema", "Video sema utilisation %"
)
igpu_engines_video_wait = Gauge(
    "igpu_engines_video_wait", "Video wait utilisation %"
)

igpu_engines_video_enhance_busy = Gauge(
    "igpu_engines_video_enhance_busy", "Video Enhance busy utilisation %"
)
igpu_engines_video_enhance_sema = Gauge(
    "igpu_engines_video_enhance_sema", "Video Enhance sema utilisation %"
)
igpu_engines_video_enhance_wait = Gauge(
    "igpu_engines_video_enhance_wait", "Video Enhance wait utilisation %"
)

igpu_engines_compute_busy = Gauge(
    "igpu_engines_compute_busy", "Compute busy utilisation %"
)
igpu_engines_compute_sema = Gauge(
    "igpu_engines_compute_sema", "Compute sema utilisation %"
)
igpu_engines_compute_wait = Gauge(
    "igpu_engines_compute_wait", "Compute wait utilisation %"
)

igpu_frequency_actual = Gauge("igpu_frequency_actual", "Frequency actual MHz")
igpu_frequency_requested = Gauge("igpu_frequency_requested", "Frequency requested MHz")

igpu_imc_bandwidth_reads = Gauge("igpu_imc_bandwidth_reads", "IMC reads MiB/s")
igpu_imc_bandwidth_writes = Gauge("igpu_imc_bandwidth_writes", "IMC writes MiB/s")

igpu_interrupts = Gauge("igpu_interrupts", "Interrupts/s")

igpu_period = Gauge("igpu_period", "Period ms")

igpu_power_gpu = Gauge("igpu_power_gpu", "GPU power W")
igpu_power_package = Gauge("igpu_power_package", "Package power W")

igpu_rc6 = Gauge("igpu_rc6", "RC6 %")


def update(data):
    igpu_engines_blitter_busy.set(
        data.get("engines", {}).get("Blitter", {}).get("busy", 0.0)
    )
    igpu_engines_blitter_sema.set(
        data.get("engines", {}).get("Blitter", {}).get("sema", 0.0)
    )
    igpu_engines_blitter_wait.set(
        data.get("engines", {}).get("Blitter", {}).get("wait", 0.0)
    )

    igpu_engines_render_3d_busy.set(
        data.get("engines", {}).get("Render/3D", {}).get("busy", 0.0)
    )
    igpu_engines_render_3d_sema.set(
        data.get("engines", {}).get("Render/3D", {}).get("sema", 0.0)
    )
    igpu_engines_render_3d_wait.set(
        data.get("engines", {}).get("Render/3D", {}).get("wait", 0.0)
    )

    igpu_engines_video_busy.set(
        data.get("engines", {}).get("Video", {}).get("busy", 0.0)
    )
    igpu_engines_video_sema.set(
        data.get("engines", {}).get("Video", {}).get("sema", 0.0)
    )
    igpu_engines_video_wait.set(
        data.get("engines", {}).get("Video", {}).get("wait", 0.0)
    )

    igpu_engines_video_enhance_busy.set(
        data.get("engines", {}).get("VideoEnhance", {}).get("busy", 0.0)
    )
    igpu_engines_video_enhance_sema.set(
        data.get("engines", {}).get("VideoEnhance", {}).get("sema", 0.0)
    )
    igpu_engines_video_enhance_wait.set(
        data.get("engines", {}).get("VideoEnhance", {}).get("wait", 0.0)
    )

    igpu_engines_compute_busy.set(
        data.get("engines", {}).get("Compute", {}).get("busy", 0.0)
    )
    igpu_engines_compute_sema.set(
        data.get("engines", {}).get("Compute", {}).get("sema", 0.0)
    )
    igpu_engines_compute_wait.set(
        data.get("engines", {}).get("Compute", {}).get("wait", 0.0)
    )

    igpu_frequency_actual.set(data.get("frequency", {}).get("actual", 0))
    igpu_frequency_requested.set(data.get("frequency", {}).get("requested", 0))

    igpu_imc_bandwidth_reads.set(data.get("imc-bandwidth", {}).get("reads", 0))
    igpu_imc_bandwidth_writes.set(data.get("imc-bandwidth", {}).get("writes", 0))

    igpu_interrupts.set(data.get("interrupts", {}).get("count", 0))

    igpu_period.set(data.get("period", {}).get("duration", 0))

    igpu_power_gpu.set(data.get("power", {}).get("GPU", 0))
    igpu_power_package.set(data.get("power", {}).get("Package", 0))

    igpu_rc6.set(data.get("rc6", {}).get("value", 0))


if __name__ == "__main__":
    if os.getenv("DEBUG", False):
        debug = logging.DEBUG
    else:
        debug = logging.INFO
    logging.basicConfig(format="%(asctime)s - %(message)s", level=debug)

    start_http_server(8080)

    period = os.getenv("REFRESH_PERIOD_MS", 10000)
    device = os.getenv("DEVICE")

    if device is not None:
        cmd = "intel_gpu_top -J -s {} -d {}".format(int(period), device)
    else:
        cmd = "intel_gpu_top -J -s {}".format(int(period))

    process = subprocess.Popen(
        cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    logging.info("Started " + cmd)
    output = ""

    object_buffer = ""
    brace_level = 0
    while process.poll() is None:
        char = process.stdout.read(1).decode("utf-8")
        if not char:
            break

        if char == '{':
            brace_level += 1

        if brace_level > 0:
            object_buffer += char

        if char == '}':
            brace_level -= 1
            if brace_level == 0 and object_buffer:
                try:
                    data = json.loads(object_buffer)
                    logging.debug(data)
                    update(data)
                except json.JSONDecodeError as e:
                    logging.error(f"JSON decode error: {e} on buffer: {object_buffer}")
                finally:
                    # Reset buffer for the next object
                    object_buffer = ""

    process.kill()

    if process.returncode != 0:
        logging.error("Error: " + process.stderr.read().decode("utf-8"))

    logging.info("Finished")