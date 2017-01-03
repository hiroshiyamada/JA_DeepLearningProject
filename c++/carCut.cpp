#include <opencv2/opencv.hpp>
#include <string>
#include <sstream>
#include <iomanip>

using namespace std;
using namespace cv;

//void detectAndDisplay(Mat image);
CvHaarClassifierCascade *cascade;
CvMemStorage            *storage;
Mat frame;
void detect(IplImage *img);

CascadeClassifier face_cascade;

int imagenum = 0;
int framenum = 0;

int main(int argc, char* argv[]){
    
    //カスケードのロード
    cascade = (CvHaarClassifierCascade*) cvLoad("./xml/cars.xml");
    storage = cvCreateMemStorage(0);
    
    //動画の読み込み
    VideoCapture video("./movies/cars.avi");
    if(!video.isOpened()){
        cout << "Video not found!" << endl;
        return -1;
    }
    
    for(;;){
        framenum++;
        video >> frame;
        if (frame.empty()) {
            cout << "End of video" << endl;
            break;
        };
        //全フレーム切りだすと画像数が増え過ぎるので50フレームごとに検出
        IplImage iplImage = frame;
        if(framenum % 50 == 0) {
            detect(&iplImage);
        }
    }
    destroyAllWindows();
    frame.release();
    video.release();
    cvReleaseHaarClassifierCascade(&cascade);
    cvReleaseMemStorage(&storage);
    return 0;
}

void detect(IplImage *img)
{
    stringstream name;
    CvSize img_size = cvGetSize(img);
    
    CvSeq *object = cvHaarDetectObjects(
                                        img,
                                        cascade,
                                        storage,
                                        1.1, //1.1,//1.5, //-------------------SCALE FACTOR
                                        2, //2        //------------------MIN NEIGHBOURS
                                        0, //0//CV_HAAR_DO_CANNY_PRUNING
                                        cvSize(30,30),//cvSize( 30,30), // ------MINSIZE
                                        img_size //cvSize(70,70)//cvSize(640,480)  //---------MAXSIZE
                                        );
    
    cout << "Total: " << object->total << " cars detected." << endl;
    for(int i = 0 ; i < ( object ? object->total : 0 ) ; i++)
    {
        CvRect *r = (CvRect*)cvGetSeqElem(object, i);
        /*cvRectangle(img,
                    cvPoint(r->x, r->y),
                    cvPoint(r->x + r->width, r->y + r->height),
                    CV_RGB(255, 0, 0), 2, 8, 0);*/
        //車部分に注目したMatをROIで作る
        Mat image = cvarrToMat(img);
        Mat carMat = image(Rect(r->x, r->y,r->width, r->height));
        //連番のファイル名を作る。
        name.str("");
        name << "./carImages/" << imagenum << ".png";
        imwrite(name.str(), carMat);
        //cvSaveImage(name.str().c_str(), img);
        imagenum++;
        
        /* デバッグ用
        cout << "Frame: " << framenum << endl;
        stringstream fname;
        fname.str("");
        fname << "./carImages/frame" << framenum << ".png";
        //imwrite(fname.str(), frame);
        cvSaveImage(fname.str().c_str(), img);
        */
    }
}
