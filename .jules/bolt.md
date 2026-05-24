## 2024-05-23 - [Canvas Animation Loop Performance]
**Learning:** The HTML specification states that `canvas.width` and `canvas.height` are `unsigned long` integers. If `window.devicePixelRatio` results in a fractional number (e.g., on a 125% or 150% scaled display), the scaled target width/height will be a float. When assigning a float to `canvas.width`, the browser truncates or rounds it to an integer. Consequently, a naive condition `canvas.width !== targetWidth` will evaluate to `true` on *every single frame* for scaled displays, falling back to the unoptimized buffer reallocation behavior.
**Action:** Always use `Math.floor()` or `Math.round()` when calculating `targetWidth` and `targetHeight` based on `window.devicePixelRatio` before comparing them to `canvas.width` and `canvas.height`.

## 2024-05-24 - [Typed Array Memory Operations]
**Learning:** For high-frequency, large-scale buffer manipulations in JavaScript (like continuous circular shifting of an audio buffer during UI interaction), manual `for` loops utilizing the modulo operator are a severe performance bottleneck because they execute per-sample within the JS engine.
**Action:** Replace such manual loops with native TypedArray methods like `Float32Array.prototype.set()` combined with `subarray()`. These methods execute near memory-copy speed at the native browser level, avoiding main thread blockage.
