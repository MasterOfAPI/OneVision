import 'dart:convert';
import 'dart:io';

import 'package:dio/dio.dart';
import 'package:file_picker/file_picker.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:image_picker/image_picker.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
import 'package:one_vision/keys.dart';
import 'package:one_vision/model/ui/snackbar.ui.model.dart';
import 'package:one_vision/screen/documents/documents_screen.dart';
import 'package:http/http.dart' as http;


class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});
  
  @override
  State<StatefulWidget> createState() => HomeState(); 

}

class HomeState extends State<HomeScreen> {

  var user = FirebaseAuth.instance.currentUser;
  
  Future<void> onQRScan() async {

    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => Scaffold(
        body : MobileScanner(
          onDetect: (capture) {
            //showSnackBar(context, "유효하지 않은 코드입니다");
            showSnackBar(context, "작성 위치 : (서울특별시 강남구 역삼동)\n날짜 : 2024-06-23\n종류 : 일반 서류");
          },
          scanWindowUpdateThreshold: 10,
        )
      ))
    );
  }

  Future<void> onScan() async {

    var picker = ImagePicker();
    var result = await picker.pickImage(source: ImageSource.camera);

    if (result == null && mounted) {
      showSnackBar(context, "파일이 스캔되지 않았습니다");
      return;
    }

    Dio dio = Dio(); 
    String uri = '$SERVER/upload';    

    String? token = await user?.getIdToken();
    Map<String, String> headers = {"Authorization" : "Bearer $token"};
    FormData body = FormData.fromMap(
      {
        "file" : await MultipartFile.fromFile(result!.path, filename: result.name)
      },
      
      ListFormat.multiCompatible,
      
    );

    try {
      final response = await dio.post(
        uri, 
        data : body, 
        options: Options(headers: headers), 
      );

      print(response.statusCode);
      
      if (response.statusCode == 200 && mounted) {    
        showSnackBar(context, "파일이 스캔되었습니다");
      }
      else {
        showSnackBar(context, "파일 스캔 실패");
      }
    } catch (error) {
      showSnackBar(context, "파일 스캔 실패");
      print(error);
    }


  }

  Future<void> onDocument() async {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => const DocumentsScreen())
    );
  }

  Future<void> onPrint() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles();

    if (result != null) {
      File file = File(result.files.single.path!);

      Dio dio = Dio(); 
      String uri = '$SERVER/process_scan_translate_print';    
      dio.options.headers["Content-Type"] = "multipart/form-data";
      String? token = await user?.getIdToken();
      Map<String, String> headers = {"Authorization" : "Bearer $token"};
      FormData body = FormData.fromMap(
        {
          "file" : await MultipartFile.fromFile(file.path, filename: file.path.split("/").last)
        },
        
        ListFormat.multiCompatible,
      );

      body.files.add(MapEntry("file", await MultipartFile.fromFile(file.path, filename: file.path.split("/").last)));


      try {
        final response = await dio.post(
          uri, 
          data : body, 
          options: Options(headers: headers), 
        );

        print(response.statusCode);
        
        if (response.statusCode == 200 && mounted) {    
          showSnackBar(context, "파일이 스캔되었습니다");
        }
        else {
          showSnackBar(context, "파일 스캔 실패");
        }
      } catch (error) {
        showSnackBar(context, "파일 스캔 실패");
        print(error);
      }
    } else {
      // User canceled the picker
    }
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