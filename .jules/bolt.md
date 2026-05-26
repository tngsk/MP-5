## 2024-05-23 - [Canvas Animation Loop Performance]
**Learning:** The HTML specification states that `canvas.width` and `canvas.height` are `unsigned long` integers. If `window.devicePixelRatio` results in a fractional number (e.g., on a 125% or 150% scaled display), the scaled target width/height will be a float. When assigning a float to `canvas.width`, the browser truncates or rounds it to an integer. Consequently, a naive condition `canvas.width !== targetWidth` will evaluate to `true` on *every single frame* for scaled displays, falling back to the unoptimized buffer reallocation behavior.
**Action:** Always use `Math.floor()` or `Math.round()` when calculating `targetWidth` and `targetHeight` based on `window.devicePixelRatio` before comparing them to `canvas.width` and `canvas.height`.

## 2024-05-24 - [Typed Array Memory Operations]
**Learning:** For high-frequency, large-scale buffer manipulations in JavaScript (like continuous circular shifting of an audio buffer during UI interaction), manual `for` loops utilizing the modulo operator are a severe performance bottleneck because they execute per-sample within the JS engine.
**Action:** Replace such manual loops with native TypedArray methods like `Float32Array.prototype.set()` combined with `subarray()`. These methods execute near memory-copy speed at the native browser level, avoiding main thread blockage.

## 2024-05-25 - [Canvas Re-rendering Optimization in requestAnimationFrame]
**Learning:** In a high-frequency `requestAnimationFrame` loop, unconditionally clearing the canvas (`ctx.clearRect`) and redrawing thousands of points (`lineTo`) is a significant CPU/GPU bottleneck, especially when the underlying data (like an audio buffer) and visualization state (like play/stop color) haven't changed.
**Action:** Always memoize canvas drawing operations. Introduce state tracking variables to compare the current frame's data/state against the previous frame, and only redraw if changes are detected. Additionally, cache DOM lookups outside the render loop.

## 2024-05-26 - [Prevent Layout Thrashing in Pointer Events]
**Learning:** Reading layout metrics like `getBoundingClientRect()` or `clientWidth` within a high-frequency `pointermove` event handler, especially immediately after mutating inline styles (`style.left`, `style.top`), causes the browser to perform forced synchronous layout (layout thrashing). This results in high CPU usage and dropped frames.
**Action:** Cache the dimensions/bounding rectangles on `pointerdown` and use the cached values during `pointermove`. Clear the cache on `pointerup` and `pointercancel`. This avoids recalculating layout during the drag operation.
