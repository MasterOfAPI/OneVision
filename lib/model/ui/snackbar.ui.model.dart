
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';

Future<void> showSnackBar(BuildContext context, String message) async {
  ScaffoldMessenger.of(context).showSnackBar(
    SnackBar(
      margin: const EdgeInsets.only(left : 20, right : 20, bottom : 30),
      behavior: SnackBarBehavior.floating,
      elevation: 0,
      content: Text(
        message,
        textAlign: TextAlign.center,
        style: TextStyle(
          fontSize: 16.sp,
          fontWeight: FontWeight.w600,
          color : const Color(0xFFFFFFFF)
        )
      ),
      backgroundColor: const Color(0xFF000000).withOpacity(0.4),
      duration: const Duration(milliseconds: 1000),
    )
  );
}