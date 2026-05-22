## 2024-05-20 - Canvas Reallocation in Render Loop
**Learning:** Setting `canvas.width` and `canvas.height` on every frame inside `requestAnimationFrame` forces a canvas buffer reallocation and clears the canvas, causing severe performance degradation even if the dimensions haven't changed.
**Action:** Always check if the computed dimensions differ from the current `canvas.width` and `canvas.height` before updating them. Use `ctx.clearRect()` to clear the canvas when dimensions haven't changed.
