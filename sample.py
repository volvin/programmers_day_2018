
from PIL import Image
import math
import random
import threading

total_rows = 20
total_cols = 20
image_filename = "/Users/scirielli/Desktop/challenge.png"
result_filename = "/Users/scirielli/Desktop/result"

empty_collected_boxes = []
empty_collected_boxes_ids = []
full_pending_boxes = []
full_pending_boxes.extend(range(0, (total_rows * total_cols)))


class MyThread(threading.Thread):
    image = None
    box_number = -1
    collected_boxes = []
    collected_boxes_ids = []
    pending_boxes = []

    def __init__(self, thread_id, name, counter, image, box_number, collected_boxes,
                 collected_boxes_ids, pending_boxes):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = name
        self.counter = counter
        self.image = image
        self.box_number = box_number
        self.collected_boxes = collected_boxes
        self.collected_boxes_ids = collected_boxes_ids
        self.pending_boxes = pending_boxes

    def run(self):
        puzzle_executor = PuzzleExecutor(self.image, self.box_number, self.collected_boxes,
                                         self.collected_boxes_ids, self.pending_boxes)
        puzzle_executor.run_process()


class PuzzleExecutor:
    box_size = 50
    safety = 5
    image = None
    box_number = -1
    collected_boxes = []
    collected_boxes_ids = []
    pending_boxes = []

    def __init__(self, image, box_number, collected_boxes, collected_boxes_ids, pending_boxes):
        self.image = image
        self.box_number = box_number
        self.collected_boxes = collected_boxes
        self.collected_boxes_ids = collected_boxes_ids
        self.pending_boxes = pending_boxes

    # main process, searches the next piece of the puzzle
    def run_process(self):
        # get surroundings (box_number)
        x1, x2, y1, y2 = self.__get_surroundings(self.box_number)
        # get matching image
        for this_box in self.pending_boxes:
            current_box = self.__get_box(self.image, this_box)
            if self.__is_a_match(current_box, x1, x2, y1, y2):
                next_box = self.box_number + 1
                if len(self.pending_boxes) == 1:
                    # puzzle resolved! merge and save the new image
                    print("Resolved! " + threading.current_thread().name)
                    self.collected_boxes.append(current_box)
                    self.__create_result_image()
                    break
                else:
                    # create a new thread and continue the search
                    try:
                        collected_boxes_copy = self.collected_boxes[:]
                        collected_boxes_copy.append(current_box)
                        collected_boxes_ids_copy = self.collected_boxes_ids[:]
                        collected_boxes_ids_copy.append(this_box)
                        pending_boxes_copy = self.pending_boxes[:]
                        pending_boxes_copy.remove(this_box)
                        new_thread_id = random.randint(1, 100)
                        new_thread = MyThread(new_thread_id, "Thread-" + str(new_thread_id), new_thread_id,
                                              self.image, next_box, collected_boxes_copy,
                                              collected_boxes_ids_copy, pending_boxes_copy)
                        new_thread.start()
                    except ValueError:
                        print(ValueError)

    def __get_surroundings(self, index):
        # get upper box
        upper_box = self.__get_upper_box(index)
        # get left box
        left_box = self.__get_left_box(index)
        # get x1, x2
        if upper_box is not None:
            x1 = self.__get_pixel(upper_box, 0 + self.safety, self.box_size - 1 - self.safety)
            x2 = self.__get_pixel(upper_box, self.box_size - 1 - self.safety, self.box_size - 1 - self.safety)
        else:
            x1, x2 = None, None
        # get y1, y2
        if left_box is not None:
            y1 = self.__get_pixel(left_box, self.box_size - 1 - self.safety, 0 + self.safety)
            y2 = self.__get_pixel(left_box, self.box_size - 1 - self.safety, self.box_size - 1 - self.safety)
        else:
            y1, y2 = None, None
        return x1, x2, y1, y2

    def __get_upper_box(self, index):
        if self.__get_row(index) == 0:  # first row
            return self.__empty_box()
        else:
            return self.collected_boxes[index - total_cols]

    def __get_left_box(self, index):
        if self.__get_col(index) == 0:  # first col
            return self.__empty_box()
        else:
            return self.collected_boxes[index - 1]

    @staticmethod
    def __get_row(index):
        decimal_part, int_part = math.modf(float(index) / float(total_cols))
        return int(int_part)

    def __get_col(self, index):
        return int(index - (self.__get_row(index) * total_cols))

    @staticmethod
    def __empty_box():
        return None

    @staticmethod
    def __get_pixel(image, i, j):
        return image.getpixel((i, j))

    def __get_box(self, original, index):
        left = self.__get_col(index) * self.box_size
        top = self.__get_row(index) * self.box_size
        right = left + self.box_size
        bottom = top + self.box_size
        return original.crop((left, top, right, bottom))

    def __is_a_match(self, box, x1, x2, y1, y2):
        p1 = self.__get_pixel(box, 0 + self.safety, self.box_size - 1 - self.safety)
        p2 = self.__get_pixel(box, 0 + self.safety, 0 + self.safety)
        p3 = self.__get_pixel(box, self.box_size - 1 - self.safety, 0 + self.safety)
        return self.__is_same_pixel(p1, y2) and self.__is_same_pixel(p2, y1) and self.__is_same_pixel(p2, x1) and self.__is_same_pixel(p3, x2)

    def __is_same_pixel(self, pixel1, pixel2):
        return (self.__is_same_value(self.__get_pixel_value(pixel1, 0), self.__get_pixel_value(pixel2, 0))
                and (self.__is_same_value(self.__get_pixel_value(pixel1, 1), self.__get_pixel_value(pixel2, 1))
                     and (self.__is_same_value(self.__get_pixel_value(pixel1, 2), self.__get_pixel_value(pixel2, 2)))))

    @staticmethod
    def __get_pixel_value(pixel, position):
        if pixel is not None:
            return pixel[position]
        else:
            return None

    @staticmethod
    def __is_same_value(value1, value2):
        if value1 is None or value1 == 0:
            value1 = 255
        if value2 is None or value2 == 0:
            value2 = 255
        return value1 == value2

    # gets all collected boxes (with no borders) and generates a new image
    def __create_result_image(self):
        border_width = 1
        box_number = 0
        new_image = Image.new('RGB', ((self.box_size - (2 * border_width)) * total_rows,
                                      (self.box_size - (2 * border_width)) * total_cols))
        for new_box in self.collected_boxes:
            pos_x = self.__get_col(box_number) * (self.box_size - (2 * border_width))
            pos_y = self.__get_row(box_number) * (self.box_size - (2 * border_width))
            new_image.paste(new_box.crop((border_width, border_width, self.box_size - border_width,
                                          self.box_size - border_width)), (pos_x, pos_y))
            box_number += 1
        file_name = result_filename + threading.current_thread().name + ".png"
        new_image.save(file_name, "PNG")
        return file_name


# open the sample image
sample_image = Image.open(image_filename)

# create the first thread and begin the puzzle search
thread1 = MyThread(1, "Thread-1", 1, sample_image, 0, empty_collected_boxes,
                   empty_collected_boxes_ids, full_pending_boxes)
thread1.start()
