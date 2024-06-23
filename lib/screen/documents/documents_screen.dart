import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:one_vision/data/document.data.dart';

class DocumentsScreen extends StatefulWidget {
  const DocumentsScreen({super.key});

  @override
  State<StatefulWidget> createState() => DocumentsState();
}

class DocumentsState extends State<DocumentsScreen> {
  List<DocumentData> data = [
    DocumentData("1", DateTime(2024, 06, 23), "pdf", "여권", "고범석의 여권 문서입니다."),
    DocumentData("1", DateTime(2024, 06, 23), "txt", "보고서", "보고서 파일입니다"),
    DocumentData("1", DateTime(2024, 06, 23), "docx", "계약서", "월세 계약서입니다"),

  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
            centerTitle: true,
            title: Text("나의 문서",
                style: TextStyle(
                  color: const Color(0xFF000000),
                  fontSize: 18.sp,
                  fontWeight: FontWeight.w800,
                ))),
        body: ListView.separated(
            itemBuilder: (context, index) {
              return Container(
                padding:
                    const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.start,
                      crossAxisAlignment: CrossAxisAlignment.center,
                      children: [
                        Image.asset(
                          (data[index].type == "pdf")
                              ? "assets/images/home/pdf.png"
                              : (data[index].type == "txt")
                                  ? "assets/images/home/txt.png"
                                  : "assets/images/home/docx.png",
                          width: 48.sp,
                          height: 48.sp,
                        ),
                        const SizedBox(
                          width: 10,
                        ),
                        Column(
                          mainAxisAlignment: MainAxisAlignment.start,
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              children: [
                                Text(data[index].kind,
                                    style: TextStyle(
                                        color: const Color(0xFF000000),
                                        fontWeight: FontWeight.w700,
                                        fontSize: 16.sp)),
                                const SizedBox(
                                  width: 4,
                                ),
                                Text(data[index].toDateString(),
                                    style: TextStyle(
                                        color: Colors.grey,
                                        fontWeight: FontWeight.w600,
                                        fontSize: 14.sp))
                              ],
                            ),
                            const SizedBox(
                              height: 5,
                            ),
                            Text(data[index].desc,
                                style: TextStyle(
                                  color: Colors.grey,
                                  fontWeight: FontWeight.w500,
                                  fontSize: 12.sp,
                                ))
                          ],
                        ),
                      ],
                    ),

                    Container(
                      padding: const EdgeInsets.symmetric(vertical: 8.5, horizontal: 10),
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(10),
                        border : Border.all(
                          color : const Color(0xFF000000),
                          width : 0.8
                        )
                      ),
                      child: Text(
                        "인쇄",
                        textAlign: TextAlign.center,
                        style : TextStyle(
                          fontSize: 16.sp,
                          fontWeight: FontWeight.w600,
                          color : const Color(0xFF000000),
                        )
                      ),
                    ),
                  ],
                ),
              );
            },
            separatorBuilder: (context, index) {
              return const SizedBox(
                height: 10,
              );
            },
            itemCount: data.length));
  }
}
