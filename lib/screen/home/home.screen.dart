import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:image_picker/image_picker.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
import 'package:one_vision/model/ui/snackbar.ui.model.dart';


class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});
  
  @override
  State<StatefulWidget> createState() => HomeState(); 

}

class HomeState extends State<HomeScreen> {
  
  Future<void> onQRScan() async {

    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => Scaffold(
        body : MobileScanner(
          onDetect: (capture) {
            showSnackBar(context, "유효하지 않은 코드입니다");
            //showSnackBar(context, "작성 위치 : (서울특별시 강남구 역삼동)\n날짜 : 2024-06-23\n종류 : 여권");
          },
          scanWindowUpdateThreshold: 2,
        )
      ))
    );
  }

  Future<void> onScan() async {
    
    var picker = ImagePicker();
    var result = await picker.pickImage(source: ImageSource.camera);

    if (result != null && mounted) {
      showSnackBar(context, "파일 스캔 완료\n종류 : 전단지");
    }
    else if (mounted) {
      showSnackBar(context, "파일이 스캔되지 않았습니다");
    }
  }

  Future<void> onDocument() async {

  }

  Future<void> onPrint() async {

  }
 
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        centerTitle: true,
        title : Text(
          "One Vision",
          style : TextStyle(
            color : const Color(0xFF000000),
            fontSize: 18.sp,
            fontWeight: FontWeight.w800,
          )
        )
      ),
      body : SingleChildScrollView(
        physics: const ClampingScrollPhysics(),
        padding: const EdgeInsets.symmetric(vertical: 30, horizontal: 16),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [

            //
            GestureDetector(
              onTap: () {
                onQRScan();
              },
              child: Container(
                width: double.infinity,
                padding: const EdgeInsets.symmetric(vertical: 13.5),
                decoration: BoxDecoration(
                  color : const Color(0xFFFFFFFF),
                  borderRadius: BorderRadius.circular(10),
                  border : Border.all(
                    color : const Color(0xFF000000),
                    width: 0.8
                  )
                ),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
              
                    Image.asset(
                      "assets/images/home/scan.png",
                      width: 32.sp,
                      height : 32.sp,
                    ),
                    
                    const SizedBox(height: 5,),
              
                    Text(
                      "문서 진위 확인",
                      style: TextStyle(
                        fontSize: 16.sp,
                        color : const Color(0xFF000000),
                        fontWeight: FontWeight.w600
                      )
                    )
                  ],
                ),
              ),
            ),

            const SizedBox(height: 10,),

            GestureDetector(
              onTap: () {
                onScan();
              },
              child: Container(
                width: double.infinity,
                padding: const EdgeInsets.symmetric(vertical: 13.5),
                decoration: BoxDecoration(
                  color : const Color(0xFFFFFFFF),
                  borderRadius: BorderRadius.circular(10),
                  border : Border.all(
                    color : const Color(0xFF000000),
                    width: 0.8
                  )
                ),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
              
                    Image.asset(
                      "assets/images/home/magnifier.png",
                      width: 32.sp,
                      height : 32.sp,
                    ),
                    
                    const SizedBox(height: 5,),
              
                    Text(
                      "문서 스캔",
                      style: TextStyle(
                        fontSize: 16.sp,
                        color : const Color(0xFF000000),
                        fontWeight: FontWeight.w600
                      )
                    )
                  ],
                ),
              ),
            ),

            const SizedBox(height: 10,),

            GestureDetector(
              onTap: () {
                onDocument();
              },
              child: Container(
                width: double.infinity,
                padding: const EdgeInsets.symmetric(vertical: 13.5),
                decoration: BoxDecoration(
                  color : const Color(0xFFFFFFFF),
                  borderRadius: BorderRadius.circular(10),
                  border : Border.all(
                    color : const Color(0xFF000000),
                    width: 0.8
                  )
                ),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
              
                    Image.asset(
                      "assets/images/home/document.png",
                      width: 32.sp,
                      height : 32.sp,
                    ),
                    
                    const SizedBox(height: 5,),
              
                    Text(
                      "내 문서 확인",
                      style: TextStyle(
                        fontSize: 16.sp,
                        color : const Color(0xFF000000),
                        fontWeight: FontWeight.w600
                      )
                    )
                  ],
                ),
              ),
            ),

            const SizedBox(height: 10,),

            GestureDetector(
              onTap: () {
                onPrint();
              },
              child: Container(
                width: double.infinity,
                padding: const EdgeInsets.symmetric(vertical: 13.5),
                decoration: BoxDecoration(
                  color : const Color(0xFFFFFFFF),
                  borderRadius: BorderRadius.circular(10),
                  border : Border.all(
                    color : const Color(0xFF000000),
                    width: 0.8
                  )
                ),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
              
                    Image.asset(
                      "assets/images/home/print.png",
                      width: 32.sp,
                      height : 32.sp,
                    ),
                    
                    const SizedBox(height: 5,),
              
                    Text(
                      "인쇄하기",
                      style: TextStyle(
                        fontSize: 16.sp,
                        color : const Color(0xFF000000),
                        fontWeight: FontWeight.w600
                      )
                    )
                  ],
                ),
              ),
            )





          ],
        ),
      ),
    );
  }
  
}