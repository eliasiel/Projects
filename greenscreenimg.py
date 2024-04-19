import cv2
import numpy as np
import matplotlib.pyplot as plt

def show_image(image):
    cv2.imshow('Cropped Image without Green', image)
    # cv2.imwrite('test.png',canvas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def draw_circle(image,center):
    radius = 20

    # Define the color of the circle in BGR format (here, we use red color)
    color = (0, 0, 255)

    # Draw the circle on the image
    cv2.circle(image, center, radius, color, thickness=2)

    # Display the image
    cv2.imshow('Circle', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def rotate(image,angle,w,h):
    center = (w // 2, h // 2)
    # Get the rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    # Apply the rotation to the image
    rotated_image = cv2.warpAffine(image, rotation_matrix, (image.shape[1], image.shape[0]))
    return rotated_image 

def get_arr_index(arr,val,axis):
   try:
        matching_index = np.min(np.where(arr[axis] == val))
   except:
    
        matching_index = np.max(np.where(arr[axis] == val))
    

   if len(arr) > 0:
        # Get the x-coordinates corresponding to the specified y-coordinate
        target_axis =''
        if axis ==1:
            target_axis=0
        else:
            target_axis=1
        matching_coordinates = arr[target_axis][matching_index]
        return matching_index
        
    
        


def auto_rotate(image,mask_w,mask_h):
    white_pix= np.where(image == 255)
    min_x =np.min(white_pix[1])
    max_x = np.max(white_pix[1])

    min_x_i = np.min(np.where(white_pix[1] == min_x)) #left
    max_x_i = np.max(np.where(white_pix[1] == max_x)) #right 

    min_y = np.min(white_pix[0]) #higset point 
    min_y_matching_x = get_arr_index(white_pix,min_y,0)
    mid_x =max_x//2

    # max_x_matching_y = get_arr_index(white_pix,max_x,0,'max')



    if min_y_matching_x<mid_x:
        rotate_dir = 'left'
    elif min_y_matching_x>mid_x:
        rotate_dir = 'right'
    print('rotate_dir: ', rotate_dir)



    
    
    w_index = mask_w
    mid_y = white_pix[0][w_index]
    
    top_right_y = np.min(white_pix[0])
    # top_left_y =white_pix[0][i]

    # top_left  = (top_left_x,top_left_y)
    # top_right = (top_right_x,top_right_y)
    # deg =0
    threshold =4
    deg = 0
    d= []
    while mid_y!=min_y+threshold:

        if rotate_dir =='right':
            deg-=000000.1
        elif rotate_dir =='left':
            deg+=000000.1
        # plt.imshow(image)

        image= rotate(image,deg,mask_w,mask_h)
        
        white_pix= np.where(image == 255)


        min_y = np.min(white_pix[0]) #higset point 
        w_index = mask_w
        mid_y = white_pix[0][w_index]
        diff = mid_y-min_y
        print('diff: ', diff)
        center = (mask_w // 2, mask_h // 2)
        # draw_circle(image,center)

        cv2.imshow('Cropped Image without Green', image)
        # cv2.imwrite('test.png',canvas)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return image
        





    # Invert the mask





def isolate_and_crop(image_path):
    # Load the image
    image = cv2.imread(image_path)

    
    # Check if the image was loaded successfully
    if image is None:
        print("Error: Unable to load image.")
        return
    
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define lower and upper bounds for green color in HSV
    lower_green = np.array([40, 40, 40])  # Narrowed lower bound
    upper_green = np.array([80, 255, 255])  # Narrowed upper bound

    # Threshold the HSV image to get only green areas
    mask = cv2.inRange(hsv, lower_green, upper_green)
    


    # Invert the mask
    mask = cv2.bitwise_not(mask)
 



    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour
    max_contour = max(contours, key=cv2.contourArea)

    # Get the bounding box of the contour
    x, y, w, h = cv2.boundingRect(max_contour)
    mask= auto_rotate(mask,w,h)

    # Crop the image using the bounding box
    cropped_image = image[y:y+h, x:x+w]

    # Create a binary mask of the same size as the cropped image
    binary_mask = np.ones((h, w), dtype=np.uint8) * 255
    binary_mask[mask[y:y+h, x:x+w] == 255] = 0

    # Create a blank canvas of the same size as the cropped image
    # cropped_image = auto_rotate(cropped_image)
    canvas = np.zeros_like(cropped_image)

    # Copy the cropped image to the canvas, excluding non-green areas
    canvas[binary_mask == 0] = cropped_image[binary_mask == 0]

    # Show the canvas with the cropped image pasted without green areas
    cv2.imshow('Cropped Image without Green', canvas)
    # cv2.imwrite('test.png',canvas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Path to the image file
image_path =r"C:\Users\elias\OneDrive\Desktop\Scan-240316-0003.jpg"
# Call the function to isolate and crop the image
isolate_and_crop(image_path)



