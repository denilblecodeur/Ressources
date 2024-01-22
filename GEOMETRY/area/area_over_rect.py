# bottom-left corner (ax1, ay1) and its top-right corner (ax2, ay2)

x_over = max(min(ax2,bx2) - max(ax1,bx1),0)
y_over = max(min(ay2,by2) - max(ay1,by1),0)

is_x_over = max(ax1, bx1) < min(ax2, bx2)
is_y_over = max(ay1, by1) < min(ay2, by2)