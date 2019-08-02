#How to USE bisect module - example

#Description:

# We have a list of points - points_list
# We would like to classify points to categories
# We have list of margins: mark_margins and its' sign value: mark_signs
# bisect.bisect_right takes mark_margins as 1st arg and one value from points as second
# bisect.bisect_right returns place where the second arg value could be inserted without breaking ascending order of mark_margins list

import bisect

points_list = [77, 76, 77, 69, 68, 64, 81, 83, 71, 74, 75, 91]
mark_signs = ["D", "C", "B", "A"]
mark_margins = [60, 70, 80, 90]  # should be in ascending order    
signs_list = [mark_signs[bisect.bisect_right(mark_margins, i) - 1] for i in points_list]

print(list(zip(points_list, signs_list)))
