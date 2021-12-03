import cv2
import imutils
import os
from animvideo import videopro1


def videopro(video,thress_val):
    path = 'static/pics'
    class CompareImage(object):

        def __init__(self, image_1_path, image_2_path):
            self.minimum_commutative_image_diff = 0.2
            self.image_1_path = image_1_path
            self.image_2_path = image_2_path

        def compare_image(self):
            image_1 = self.image_1_path
            image_2 = self.image_2_path
            commutative_image_diff = self.get_image_difference(image_1, image_2)

            if commutative_image_diff < self.minimum_commutative_image_diff:
                return 1
            return 0 

        @staticmethod
        def get_image_difference(image_1, image_2):
            first_image_hist = cv2.calcHist([image_1], [0], None, [256], [0, 256])
            second_image_hist = cv2.calcHist([image_2], [0], None, [256], [0, 256])

            img_hist_diff = cv2.compareHist(first_image_hist, second_image_hist, cv2.HISTCMP_BHATTACHARYYA)
            img_template_probability_match = cv2.matchTemplate(first_image_hist, second_image_hist, cv2.TM_CCOEFF_NORMED)[0][0]
            img_template_diff = 1 - img_template_probability_match

            # taking only 10% of histogram diff, since it's less accurate than template method
            commutative_image_diff = (img_hist_diff / 10) + img_template_diff
            return commutative_image_diff
    cap = cv2.VideoCapture(video)
    images = []


    if (cap.isOpened()== False):
        
        print("Cannot open the file")

    old_frame = None
    last_frame = None
    i = 0
    j = 0
    #no_frame = 0
    while (cap.isOpened()):

        ret, frame = cap.read()
        
        if j == 0:
            first = imutils.resize(frame, width=450)
            cv2.imwrite(os.path.join(path,str(i)+'.jpg'),first)
            i = 1
            j=1
        

        if ret == True:
            #print(no_frame)
            #no_frame = no_frame+1

            frame = imutils.resize(frame, width=450)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if old_frame is not None:
                
                diff = cv2.absdiff(old_frame,gray)
                #cv2.imshow("diff",diff)
                _, th = cv2.threshold(diff, 80, 200, cv2.THRESH_BINARY)
                cnts,hierarchy = cv2.findContours(th.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)


                
                for contor in cnts:  
                    if cv2.contourArea(contor) > thress_val     :
                        compare_image = CompareImage(gray, old_frame)
                        image_difference = compare_image.compare_image()
                        
                        if image_difference == 0:
                            #cv2.imwrite('image'+str(i)+'.jpg',frame)
                            images.append(frame)

                        i+=1

                
            old_frame = gray
            last_frame = frame


        else:
            print('Completed')

            break


    #print(len(images))
    count = 1

    for i in range (0,len(images)-1):
        compare_image = CompareImage(images[i],images[i+1])
        image_difference = compare_image.compare_image()
        if image_difference == 0:
            cv2.imwrite(os.path.join(path,str(count)+'.jpg'),images[i])
            count += 1
    if(len(images)>=1):
        cv2.imwrite(os.path.join(path,str(count)+'.jpg'),images[len(images)-1])

    if(count<=3):
        videopro1(video)
    
    cv2.imwrite(os.path.join(path,str(100)+'.jpg'),last_frame)
    

#videolink = 'test video 1.mp4'
#videopro(videolink)

