import tkinter.font as tkFont

def draw_wrapped_text(x, y, width, height, text, font_name="Myanmar Text", font_size=10):
    font = tkFont.Font(family=font_name, size=font_size)
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + " " + word if current_line else word
        if font.measure(test_line) <= width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    # Draw lines in two columns if needed
    max_lines_per_col = height // font.metrics("linespace")
    col_x_offsets = [x - width//2 + 5, x + width//2 + 5]  # left and right columns
    col_y = y - height//2 + 10

    for i, line in enumerate(lines):
        col = i // max_lines_per_col
        row = i % max_lines_per_col
        if col < 2:
            canvas.create_text(col_x_offsets[col], col_y + row * font.metrics("linespace"),
                               text=line, font=(font_name, font_size), anchor="nw", fill="black")