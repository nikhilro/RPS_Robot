import math

WHITE = 1
BLACK = 0

#This method returns the prefix sum array for a given 2D array
def prefix_sum_array (array):
    prefix_sum = [[0 for x in range(len(array[0])+1) ] for y in range(len(array)+1)]
    for a in range(1, len(array)+1):
        for b in range(1, len(array[a-1])+1):
            prefix_sum[a][b] = prefix_sum[a-1][b] + prefix_sum[a][b-1] - prefix_sum[a-1][b-1] + array[a-1][b-1]
    return prefix_sum

#This method returns the sum of a given block in a 2D array
def find_sum (prefix_sum, left_row, left_coloumn, right_row, right_coloumn):
    if left_row >= right_row or left_coloumn >= right_coloumn:
        return 0

    p_sum = prefix_sum[left_row][left_coloumn] + prefix_sum[right_row][right_coloumn]
    p_sum -= prefix_sum[right_row][left_coloumn] + prefix_sum[left_row][right_coloumn]
    return p_sum

#This method finds the average of a given block in a 2D array
def average (array_2d, start_x, end_x, start_y, end_y):
    total = 0
    count = 0
    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            total += array_2d[x][y]
            count += 1
    return total/count

def percent_white (img_array):
    total_squares = 0
    white_squares = 0
    for x in img_array:
        for a in range(len(x)):
            total_squares += 1
            if x[a] == WHITE:
                white_squares += 1
    return white_squares/total_squares

#This method returns an image converted to black and white by finding the middle colour and considering everything above the middle to be white
def to_black_white (img_array):
    min = img_array[0][0]
    max = img_array[0][0]
    for x in img_array:
        for a in range(len(x)):
            min = x[a] if x[a] < min else min
            max = x[a] if x[a] > max else max

    border = (min + max)/2

    img_cpy = [[0 for x in range(len(img_array[0]))] for y in range(len(img_array))]
    for a in range(len(img_array)):
        for b in range(len(img_array[a])):
            img_cpy[a][b] = WHITE if img_array[a][b] >= border else BLACK
    return img_cpy

#This method compresses an image to 50x50 size
def compress_to_50x50 (img_array):
    length = len(img_array)
    height = len(img_array[0])
    arr = [[0 for x in range(50)] for y in range(50)]
    if length < 50 or height < 50:
        return img_array

    prev_x = 0
    prev_y = 0
    curr_x = 0
    curr_y = 0
    for x in range(1, 51):
        curr_x = length*x//50
        for y in range(1, 51):
            prev_y = curr_y
            curr_y = height*y//50
            arr[y-1][x-1] = average(img_array, prev_x, curr_x, prev_y, curr_y)

        prev_x = curr_x
        curr_y = 0
    return arr
    prev_x = 0
    prev_y = 0
    curr_x = 0
    curr_y = 0
    for x in range(1, 51):
        curr_x = length*x//50
        for y in range(1, 51):
            prev_y = curr_y
            curr_y = height*y//50
            arr[y-1][x-1] = average(img_array, prev_x, curr_x, prev_y, curr_y)

        prev_x = curr_x
        curr_y = 0
    return arr

#This method crops the image to the hand only by finding the palm (largest square) and takes everything to the left and up of the palm
def crop_to_hand (img_array):
    img = to_black_white(img_array)
    n_w = percent_white(img)*(len(img_array)*len(img_array[0]))

    c_size = int(math.sqrt(n_w))
    threshold = 0.9

    p_sum = prefix_sum_array(img)

    right_x = 0
    right_y = 0
    size = 0
    found = False

    while c_size > 0:
        for a in reversed(range(c_size-1, len(img))):
            for b in reversed(range(c_size-1, len(img[a]))):
                p_s = find_sum(p_sum, a - c_size + 1, b - c_size + 1, a + 1, b + 1)
                '''num_white calculated by (all black matrix - actual matrix = only white matrix with entries BLACK-WHITE)
                EG: |B B|   |B W|                            |0 B-W|
                    |B B| - |B B| = |all black| - |actual| = |0 0  |
                '''
                n_w = (c_size*c_size*(BLACK) - p_s)/(BLACK-WHITE)
                if (n_w/(c_size*c_size)) >= threshold:
                    right_y = a
                    right_x = b
                    size = c_size
                    found = True
                    break
            if found:
                break
        if found:
            break
        else:
            c_size -= 1

    min_x = right_x;
    min_y = right_y;
    for a in range(right_y):
        for b in range(right_x):
            if img[a][b] == WHITE:
                min_x = b if b < min_x else min_x
                min_y = a if a < min_y else min_y

    cropped_img = [[0 for x in range(min_x, right_x+1)] for y in range(min_y, right_y+1)]
    for a in range(min_y, right_y+1):
        for b in range(min_x, right_x+1):
            cropped_img[a-min_y][b-min_x] = img_array[a][b]

    return cropped_img

#This method converts an image array into a 50x50 black white img of the hand only
def convert_img_to_bw_hand_50x50 (img_array):
    img = crop_to_hand(img_array)
    img = compress_to_50x50(img)
    img = to_black_white(img)
    return img

test = convert_img_to_bw_hand_50x50\
                    ([[0, 1, 1, 1, 0],
                      [0, 0, 1, 1, 0],
                      [1, 0, 1, 1, 0],
                      [0, 0, 0, 0, 0]])
for a in test:
    print(a)
