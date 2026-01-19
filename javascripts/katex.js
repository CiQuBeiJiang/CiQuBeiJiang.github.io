document$.subscribe(({ body }) => {
  renderMathInElement(body, {
    delimiters: [
      { left: "$$",  right: "$$",  display: true },  // 你的块级公式用这个，核心生效
      { left: "$",   right: "$",   display: false },  // 行内公式，保留
      { left: "\\(", right: "\\)", display: false },
      { left: "\\[", right: "\\]", display: true }
    ],
    strict: false 
  })
})