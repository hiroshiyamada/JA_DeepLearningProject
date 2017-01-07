#include <opencv2/opencv.hpp>
#include <string>
#include <sstream>
#include <iomanip>

using namespace std;
using namespace cv;

void detectAndDisplay(Mat image);

CascadeClassifier face_cascade;

int imagenum = 0;

int main(int argc, char* argv[]){
  int framenum = 0;

  //カスケードのロード
  face_cascade.load("lbpcascade_animeface.xml");

  //動画の読み込み
  Mat frame;
  VideoCapture video("video.mp4");
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
    //全フレーム切りだすと画像数が増え過ぎるので10フレームごとに検出
    if(framenum%10==0) detectAndDisplay(frame);
  }
  return 0;
}

//認識と表示を行う関数
void detectAndDisplay(Mat image)
{
  vector<Rect> faces;
  Mat frame_gray;
  stringstream name;

  //画像のグレースケール化
  cvtColor(image, frame_gray, COLOR_BGR2GRAY );
  //ヒストグラムの平坦化
  equalizeHist(frame_gray, frame_gray);
  //顔の認識　小さい顔は除外
  face_cascade.detectMultiScale(frame_gray, faces, 1.1, 3, 0, Size(80,80));
  for(int i = 0; i<faces.size(); i++){
    //顔部分に注目したMatをROIで作る
    Mat Face = image(Rect(faces[i].x, faces[i].y,faces[i].width, faces[i].height));
    //連番のファイル名を作る。参考：http://www.geocities.jp/eneces_jupiter_jp/cpp1/013-001.html
    name.str("");
    name << "image" << setw(3) << setfill('0') << imagenum << ".png";
    imwrite(name.str(), Face);
    imagenum++;
  }
}