"""Processing-style canvas sketches for the public Streamlit website."""

from __future__ import annotations

import json
from html import escape
from typing import Any

import streamlit as st
import streamlit.components.v1 as components


def render_processing_sketch(
    sketch: str,
    payload: dict[str, Any],
    title: str,
    summary: str,
    height: int = 420,
) -> None:
    """Render a responsive p5-style canvas component with fallback text."""

    safe_title = escape(title)
    safe_summary = escape(summary)
    data = json.dumps(payload)
    html = f"""
    <section class="processing-frame" aria-label="{safe_title}">
      <div class="processing-caption">
        <strong>{safe_title}</strong>
        <span>{safe_summary}</span>
      </div>
      <canvas id="processing-canvas"></canvas>
      <script>
      const payload = {data};
      const canvas = document.getElementById("processing-canvas");
      const ctx = canvas.getContext("2d");
      const frame = canvas.closest(".processing-frame");
      const sketch = "{escape(sketch)}";
      const colors = {{
        navy: "#123447",
        deep: "#0b2533",
        ice: "#67d0df",
        teal: "#25b99a",
        amber: "#d8a24a",
        purple: "#8ea7ff",
        red: "#d66a6a",
        white: "#f2f5f6",
        muted: "rgba(242,245,246,0.58)"
      }};

      function setupCanvas() {{
        const rect = frame.getBoundingClientRect();
        const ratio = window.devicePixelRatio || 1;
        canvas.width = Math.max(320, rect.width) * ratio;
        canvas.height = {height} * ratio;
        canvas.style.width = "100%";
        canvas.style.height = "{height}px";
        ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
      }}

      function clear() {{
        const w = canvas.clientWidth;
        const h = canvas.clientHeight;
        const grad = ctx.createLinearGradient(0, 0, w, h);
        grad.addColorStop(0, colors.deep);
        grad.addColorStop(1, colors.navy);
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, w, h);
        return [w, h];
      }}

      function text(label, x, y, size=13, color=colors.white, align="center", weight=600) {{
        ctx.fillStyle = color;
        ctx.font = `${{weight}} ${{size}}px system-ui, -apple-system, Segoe UI, sans-serif`;
        ctx.textAlign = align;
        ctx.textBaseline = "middle";
        ctx.fillText(label, x, y);
      }}

      function roundRect(x, y, w, h, r, fill, stroke=null) {{
        ctx.beginPath();
        ctx.moveTo(x + r, y);
        ctx.lineTo(x + w - r, y);
        ctx.quadraticCurveTo(x + w, y, x + w, y + r);
        ctx.lineTo(x + w, y + h - r);
        ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
        ctx.lineTo(x + r, y + h);
        ctx.quadraticCurveTo(x, y + h, x, y + h - r);
        ctx.lineTo(x, y + r);
        ctx.quadraticCurveTo(x, y, x + r, y);
        ctx.closePath();
        ctx.fillStyle = fill;
        ctx.fill();
        if (stroke) {{
          ctx.strokeStyle = stroke;
          ctx.lineWidth = 1.2;
          ctx.stroke();
        }}
      }}

      function arrow(x1, y1, x2, y2, color=colors.muted) {{
        ctx.strokeStyle = color;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        ctx.stroke();
        const a = Math.atan2(y2-y1, x2-x1);
        ctx.beginPath();
        ctx.moveTo(x2, y2);
        ctx.lineTo(x2 - 9 * Math.cos(a - 0.45), y2 - 9 * Math.sin(a - 0.45));
        ctx.lineTo(x2 - 9 * Math.cos(a + 0.45), y2 - 9 * Math.sin(a + 0.45));
        ctx.closePath();
        ctx.fillStyle = color;
        ctx.fill();
      }}

      function drawSystemFlow(t, w, h) {{
        const compact = w < 620;
        const y = compact ? [85, 205, 325] : [h * 0.55, h * 0.55, h * 0.55];
        const x = compact ? [w * 0.5, w * 0.5, w * 0.5] : [w * 0.18, w * 0.5, w * 0.82];
        text("Constraining North Slope Gas Hydrates", w / 2, 32, compact ? 19 : 24);
        text("Public geology + approved logs + physics-constrained ML", w / 2, 62, 13, colors.muted);
        ctx.strokeStyle = colors.ice;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(x[0] - 75, y[0] - 35);
        ctx.lineTo(x[0] - 15, y[0] - 55);
        ctx.lineTo(x[0] + 70, y[0] - 26);
        ctx.lineTo(x[0] + 55, y[0] + 40);
        ctx.lineTo(x[0] - 55, y[0] + 50);
        ctx.closePath();
        ctx.stroke();
        for (let i = 0; i < 14; i++) {{
          const px = x[0] - 62 + (i % 5) * 29 + Math.sin(t / 28 + i) * 2;
          const py = y[0] - 34 + Math.floor(i / 5) * 29;
          ctx.fillStyle = i % 3 === 0 ? colors.teal : colors.ice;
          ctx.beginPath();
          ctx.arc(px, py, 3.5 + Math.sin(t / 20 + i) * 1.2, 0, Math.PI * 2);
          ctx.fill();
        }}
        for (let i = 0; i < 6; i++) {{
          const tx = x[1] - 72 + i * 28;
          ctx.strokeStyle = payload.tracks?.[i]?.color || colors.white;
          ctx.lineWidth = 2;
          ctx.beginPath();
          for (let yy = y[1] - 78; yy <= y[1] + 78; yy += 8) {{
            const xx = tx + Math.sin(yy / 22 + t / 38 + i) * 8;
            yy === y[1] - 78 ? ctx.moveTo(xx, yy) : ctx.lineTo(xx, yy);
          }}
          ctx.stroke();
        }}
        ctx.strokeStyle = colors.white;
        ctx.lineWidth = 1.3;
        ctx.strokeRect(x[1] - 88, y[1] - 82, 176, 164);
        ctx.fillStyle = "rgba(216,162,74,0.22)";
        ctx.fillRect(x[1] - 88, y[1] + 4, 176, 34);
        roundRect(x[2] - 94, y[2] - 82, 188, 164, 12, "rgba(242,245,246,0.08)", colors.muted);
        ["Detect", "Saturation", "Uncertainty", "Rank"].forEach((label, i) => {{
          roundRect(x[2] - 72, y[2] - 58 + i * 35, 144, 24, 8, "rgba(103,208,223,0.12)", i === 2 ? colors.amber : colors.teal);
          text(label, x[2], y[2] - 46 + i * 35, 12);
        }});
        if (compact) {{
          arrow(x[0], y[0] + 65, x[1], y[1] - 95, colors.teal);
          arrow(x[1], y[1] + 95, x[2], y[2] - 95, colors.teal);
        }} else {{
          arrow(x[0] + 98, y[0], x[1] - 112, y[1], colors.teal);
          arrow(x[1] + 112, y[1], x[2] - 112, y[2], colors.teal);
        }}
        text("Regional context", x[0], y[0] + 86, 12, colors.ice);
        text("Well evidence", x[1], y[1] + 104, 12, colors.ice);
        text("Interval decisions", x[2], y[2] + 104, 12, colors.ice);
      }}

      function drawPipeline(t, w, h) {{
        const stages = payload.stages || [];
        const compact = w < 680;
        text(payload.heading || "Data to Decision", w / 2, 34, 22);
        stages.forEach((stage, i) => {{
          const x = compact ? w * 0.5 : 70 + i * ((w - 140) / Math.max(1, stages.length - 1));
          const y = compact ? 80 + i * 48 : h * 0.55;
          if (i > 0) {{
            const px = compact ? w * 0.5 : 70 + (i - 1) * ((w - 140) / Math.max(1, stages.length - 1));
            const py = compact ? 80 + (i - 1) * 48 : h * 0.55;
            arrow(px + (compact ? 0 : 33), py + (compact ? 20 : 0), x - (compact ? 0 : 33), y - (compact ? 20 : 0), colors.muted);
          }}
          const r = 24 + Math.sin(t / 30 + i) * 2;
          ctx.fillStyle = "rgba(255,255,255,0.08)";
          ctx.beginPath();
          ctx.arc(x, y, r + 7, 0, Math.PI * 2);
          ctx.fill();
          ctx.fillStyle = stage.color;
          ctx.beginPath();
          ctx.arc(x, y, r, 0, Math.PI * 2);
          ctx.fill();
          text(String(i + 1), x, y, 16, colors.deep, "center", 800);
          text(stage.label, x, y + 45, 12);
          text(stage.status, x, y + 63, 10, colors.muted);
        }});
      }}

      function drawEvidenceStack(t, w, h) {{
        const stack = payload.stack || [];
        text("Subsurface Evidence Stack", w / 2, 34, 22);
        const left = w * 0.12;
        const right = w * 0.88;
        const top = 80;
        const layerH = Math.min(66, (h - 150) / Math.max(1, stack.length));
        stack.forEach((row, i) => {{
          const y = top + i * (layerH + 12);
          const wave = Math.sin(t / 45 + i) * 8;
          ctx.fillStyle = `rgba(${{i === 0 ? "103,208,223" : i === 1 ? "37,185,154" : i === 2 ? "216,162,74" : "142,167,255"}},0.13)`;
          ctx.beginPath();
          ctx.moveTo(left, y + 10);
          for (let x = left; x <= right; x += 18) {{
            ctx.lineTo(x, y + 10 + Math.sin(x / 48 + t / 60 + i) * (5 + i * 1.5));
          }}
          ctx.lineTo(right, y + layerH);
          ctx.lineTo(left, y + layerH);
          ctx.closePath();
          ctx.fill();
          ctx.strokeStyle = row.color;
          ctx.lineWidth = 1.8;
          ctx.stroke();
          if (i === 2) {{
            for (let j = 0; j < 6; j++) {{
              const tx = left + 70 + j * 48;
              ctx.strokeStyle = payload.tracks?.[j]?.color || colors.white;
              ctx.lineWidth = 1.6;
              ctx.beginPath();
              ctx.moveTo(tx, y + 8);
              ctx.lineTo(tx + Math.sin(t / 34 + j) * 8, y + layerH - 8);
              ctx.stroke();
            }}
          }}
          if (i === 3) {{
            ["phase", "sat", "uncertainty", "rank"].forEach((label, j) => {{
              roundRect(right - 245 + j * 58, y + 18, 52, 24, 7, "rgba(242,245,246,0.08)", row.color);
              text(label, right - 219 + j * 58, y + 30, 9, colors.white);
            }});
          }}
          text(row.label, left + 14, y + layerH / 2, 13, row.color, "left", 800);
          text(row.detail, left + 190, y + layerH / 2, 11, colors.muted, "left");
          if (i < stack.length - 1) arrow(w / 2, y + layerH + 2, w / 2, y + layerH + 12, colors.muted);
        }});
        text("Regional maps constrain confidence; logs/core decide intervals.", w / 2, h - 28, 12, colors.muted);
      }}

      function drawLayerMap(t, w, h) {{
        text("Public North Slope Layers", w / 2, 34, 22);
        const cx = w * 0.42;
        const cy = h * 0.48;
        ctx.strokeStyle = colors.ice;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(cx - 165, cy - 42);
        ctx.bezierCurveTo(cx - 90, cy - 95, cx + 60, cy - 78, cx + 160, cy - 34);
        ctx.lineTo(cx + 130, cy + 55);
        ctx.bezierCurveTo(cx + 32, cy + 92, cx - 106, cy + 82, cx - 170, cy + 34);
        ctx.closePath();
        ctx.stroke();
        for (let i = 0; i < 80; i++) {{
          const px = cx - 145 + ((i * 41) % 285);
          const py = cy - 48 + ((i * 29) % 96);
          ctx.fillStyle = i % 7 === 0 ? colors.amber : colors.ice;
          ctx.globalAlpha = 0.42 + 0.22 * Math.sin(t / 28 + i);
          ctx.beginPath();
          ctx.arc(px, py, i % 7 === 0 ? 2.6 : 1.8, 0, Math.PI * 2);
          ctx.fill();
        }}
        ctx.globalAlpha = 1;
        (payload.layers || []).slice(0, 5).forEach((layer, i) => {{
          const x = w * 0.72;
          const y = 92 + i * 48;
          roundRect(x - 88, y - 15, 176, 30, 8, "rgba(242,245,246,0.08)", layer.color);
          text(layer.label, x - 76, y, 11, colors.white, "left");
          text(String(layer.value), x + 72, y, 12, layer.color, "right", 800);
        }});
      }}

      function drawStructure(t, w, h) {{
        text("Structural Stack Preview", w / 2, 34, 22);
        const layers = payload.layers || [];
        layers.forEach((layer, i) => {{
          const y = 98 + layer.depth * (h - 150);
          const amp = 16 + i * 4;
          ctx.strokeStyle = layer.color;
          ctx.lineWidth = 3;
          ctx.beginPath();
          for (let x = w * 0.12; x <= w * 0.78; x += 14) {{
            const yy = y + Math.sin(x / 58 + t / 55 + i) * amp;
            x === w * 0.12 ? ctx.moveTo(x, yy) : ctx.lineTo(x, yy);
          }}
          ctx.stroke();
          text(layer.label, w * 0.84, y, 12, layer.color, "left");
        }});
        for (let i = 0; i < 9; i++) {{
          const x = w * 0.16 + i * (w * 0.058);
          ctx.strokeStyle = i % 3 === 0 ? colors.amber : colors.muted;
          ctx.lineWidth = 1.2;
          ctx.beginPath();
          ctx.moveTo(x, 86);
          ctx.lineTo(x + Math.sin(t / 45 + i) * 9, h - 55);
          ctx.stroke();
          ctx.fillStyle = colors.ice;
          ctx.beginPath();
          ctx.arc(x, 86, 3, 0, Math.PI * 2);
          ctx.fill();
        }}
        text("Wells and public horizons only", w / 2, h - 28, 12, colors.muted);
      }}

      function drawWellEvidence(t, w, h) {{
        const tracks = payload.tracks || [];
        text("Synthetic Well Evidence", w / 2, 28, 22);
        const left = Math.max(28, w * 0.08);
        const top = 65;
        const trackW = Math.min(70, (w * 0.58) / Math.max(1, tracks.length));
        tracks.forEach((track, i) => {{
          const x = left + i * (trackW + 8);
          roundRect(x, top, trackW, h - 115, 8, "rgba(242,245,246,0.05)", "rgba(242,245,246,0.25)");
          ctx.strokeStyle = track.color;
          ctx.lineWidth = 2;
          ctx.beginPath();
          for (let y = top + 12; y < h - 62; y += 8) {{
            const xx = x + trackW * 0.5 + Math.sin(y / 24 + t / 38 + track.phase) * (trackW * 0.28);
            y === top + 12 ? ctx.moveTo(xx, y) : ctx.lineTo(xx, y);
          }}
          ctx.stroke();
          text(track.label, x + trackW / 2, h - 42, 11, track.color);
        }});
        ctx.fillStyle = "rgba(216,162,74,0.25)";
        ctx.fillRect(left, top + (h - 150) * 0.46, tracks.length * (trackW + 8) - 8, 42);
        ctx.strokeStyle = colors.amber;
        ctx.strokeRect(left, top + (h - 150) * 0.46, tracks.length * (trackW + 8) - 8, 42);
        const domains = payload.domains || [];
        const rx = Math.min(w - 130, left + tracks.length * (trackW + 8) + 98);
        const ry = h * 0.48;
        domains.forEach((d, i) => {{
          const a = -Math.PI / 2 + i * Math.PI * 2 / domains.length;
          const r = 36 + d.value * 54;
          ctx.strokeStyle = d.color;
          ctx.lineWidth = 5;
          ctx.beginPath();
          ctx.arc(rx + Math.cos(a) * 62, ry + Math.sin(a) * 62, 15, -Math.PI / 2, -Math.PI / 2 + d.value * Math.PI * 2);
          ctx.stroke();
          text(d.label, rx + Math.cos(a) * 100, ry + Math.sin(a) * 92, 10, colors.muted);
          ctx.fillStyle = d.color;
          ctx.beginPath();
          ctx.arc(rx + Math.cos(a) * r, ry + Math.sin(a) * r, 3, 0, Math.PI * 2);
          ctx.fill();
        }});
        text("Interval review", rx, ry, 13, colors.white, "center", 800);
      }}

      function drawBoundary(t, w, h) {{
        text("Inputs, Features, Targets", w / 2, 34, 22);
        const items = payload.items || [];
        items.forEach((item, i) => {{
          const x = 85 + i * ((w - 170) / Math.max(1, items.length - 1));
          const y = h * 0.5;
          roundRect(x - 62, y - 30, 124, 60, 10, "rgba(242,245,246,0.08)", item.color);
          text(item.label, x, y, 12, colors.white);
          if (i > 0) arrow(85 + (i - 1) * ((w - 170) / Math.max(1, items.length - 1)) + 68, y, x - 68, y, i === 3 ? colors.red : colors.muted);
        }});
        ctx.strokeStyle = colors.red;
        ctx.lineWidth = 3;
        ctx.setLineDash([8, 6]);
        ctx.beginPath();
        ctx.moveTo(w * 0.68, h * 0.24);
        ctx.lineTo(w * 0.68, h * 0.78);
        ctx.stroke();
        ctx.setLineDash([]);
        text("target leakage barrier", w * 0.68 + 12, h * 0.23, 11, colors.red, "left");
      }}

      function drawCohort(t, w, h) {{
        text("Whole-Well Validation", w / 2, 34, 22);
        const split = payload.split || [];
        const total = split.reduce((sum, row) => sum + row.count, 0);
        let x = 42;
        split.forEach(row => {{
          const bw = Math.max(58, (w - 84) * row.count / total);
          roundRect(x, h * 0.43, bw - 8, 66, 8, "rgba(242,245,246,0.08)", row.color);
          text(row.label, x + (bw - 8) / 2, h * 0.43 + 24, 11, colors.white);
          text(String(row.count), x + (bw - 8) / 2, h * 0.43 + 46, 18, row.color, "center", 800);
          x += bw;
        }});
        text("Depth rows stay inside their wells during split", w / 2, h - 36, 12, colors.muted);
      }}

      function drawBuiltNext(t, w, h) {{
        text("Built Now -> Activate With Approved Data", w / 2, 34, 21);
        const built = payload.built || [];
        const next = payload.next || [];
        const compact = w < 680;
        built.forEach((label, i) => {{
          const x1 = compact ? w * 0.5 : w * 0.29;
          const x2 = compact ? w * 0.5 : w * 0.71;
          const y1 = 82 + i * 50;
          const y2 = compact ? y1 + 245 : y1;
          roundRect(x1 - 112, y1 - 17, 224, 34, 8, "rgba(37,185,154,0.18)", colors.teal);
          text(label, x1, y1, 12);
          if (next[i]) {{
            roundRect(x2 - 112, y2 - 17, 224, 34, 8, "rgba(103,208,223,0.08)", colors.ice);
            text(next[i], x2, y2, 12);
            arrow(x1 + (compact ? 0 : 118), y1 + (compact ? 22 : 0), x2 - (compact ? 0 : 118), y2 - (compact ? 22 : 0), colors.muted);
          }}
        }});
      }}

      function drawBlocks(t, w, h) {{
        text(payload.heading || "Project Blocks", w / 2, 34, 22);
        const rows = payload.rows || [];
        rows.forEach((row, i) => {{
          const x = 60 + (i % 3) * ((w - 120) / 3);
          const y = 86 + Math.floor(i / 3) * 82;
          roundRect(x, y, (w - 150) / 3, 60, 8, "rgba(242,245,246,0.08)", row.severity === "waiting" ? colors.amber : colors.ice);
          text(row.label, x + 14, y + 22, 12, colors.white, "left", 800);
          text(row.affects || row.status || "", x + 14, y + 42, 10, colors.muted, "left");
        }});
      }}

      function draw(t=0) {{
        const [w, h] = clear();
        if (sketch === "system_flow") drawSystemFlow(t, w, h);
        else if (sketch === "pipeline") drawPipeline(t, w, h);
        else if (sketch === "evidence_stack") drawEvidenceStack(t, w, h);
        else if (sketch === "layer_map") drawLayerMap(t, w, h);
        else if (sketch === "structure_stack") drawStructure(t, w, h);
        else if (sketch === "well_evidence") drawWellEvidence(t, w, h);
        else if (sketch === "target_boundary") drawBoundary(t, w, h);
        else if (sketch === "cohort_split") drawCohort(t, w, h);
        else if (sketch === "built_next") drawBuiltNext(t, w, h);
        else if (sketch === "blocks") drawBlocks(t, w, h);
        requestAnimationFrame(draw);
      }}

      setupCanvas();
      window.addEventListener("resize", setupCanvas);
      requestAnimationFrame(draw);
      </script>
      <style>
        .processing-frame {{
          background: #123447;
          border: 1px solid rgba(103,208,223,0.32);
          border-radius: 8px;
          box-shadow: 0 14px 34px rgba(18,52,71,0.15);
          margin: 0.45rem 0 1rem;
          overflow: hidden;
        }}
        .processing-caption {{
          align-items: baseline;
          background: rgba(11,37,51,0.86);
          border-bottom: 1px solid rgba(103,208,223,0.28);
          color: #f2f5f6;
          display: flex;
          gap: 0.75rem;
          justify-content: space-between;
          padding: 0.65rem 0.85rem;
        }}
        .processing-caption span {{
          color: rgba(242,245,246,0.72);
          font-size: 0.84rem;
          text-align: right;
        }}
        @media (max-width: 680px) {{
          .processing-caption {{
            align-items: flex-start;
            flex-direction: column;
            gap: 0.25rem;
          }}
          .processing-caption span {{
            text-align: left;
          }}
        }}
      </style>
    </section>
    """
    components.html(html, height=height + 52, scrolling=False)
    st.caption(summary)
