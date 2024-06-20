import 'dart:developer';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:google_sign_in/google_sign_in.dart';
import 'package:sign_in_with_apple/sign_in_with_apple.dart';

import 'package:flutter/material.dart';

class SignInScreen extends StatefulWidget {
  const SignInScreen({super.key});

  @override
  State<StatefulWidget> createState() => SignInState();
}

class SignInState extends State<SignInScreen> {

  Future<void> signInApple(BuildContext context) async {   
    try {
      final appleCredential = await SignInWithApple.getAppleIDCredential(scopes: [
        AppleIDAuthorizationScopes.email,
        AppleIDAuthorizationScopes.fullName,
      ]);
      final oauthCrendential = OAuthProvider("apple.com").credential(
        idToken: appleCredential.identityToken,
        accessToken: appleCredential.authorizationCode,
      );

      var user = await FirebaseAuth.instance.signInWithCredential(oauthCrendential);
      var token = await user.user?.getIdToken();

      return;
    } 
    on FirebaseAuthException catch (e) {
      log("파이어 베이스 로그인 에러 : $e");
      return;
    } catch (e) {
      log("애플 로그인 에러 : $e");
      return;
    }
  }

  Future<void> signInGoogle(BuildContext context) async{

    GoogleSignInAccount? googleUser;

    try {
      googleUser = await GoogleSignIn().signIn();
    } on Exception catch (e) {
      debugPrint(e.toString());    
    }

    if (googleUser != null) {    
      try {

        final GoogleSignInAuthentication googleAuth = await googleUser.authentication;
        final credential = GoogleAuthProvider.credential(
          accessToken: googleAuth.accessToken,
          idToken: googleAuth.idToken,
        );

        var user = await FirebaseAuth.instance.signInWithCredential(credential);
        var token = await user.user?.getIdToken();
        
        return;
      } 
      on FirebaseAuthException catch (e) {
        log("파이어 베이스 로그인 에러 : $e");
        return;
      } catch (e) {
        log("애플 로그인 에러 : $e");
        return;
      }
    }
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body : Container(
        width: MediaQuery.of(context).size.width,
        height : MediaQuery.of(context).size.height,
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 30),
        decoration: const BoxDecoration(
          color : Color(0xFFFFFFFF),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [

            const SizedBox.shrink(),

            const Text(
              "원 비전",
              style : TextStyle(
                color : Color(0xFF000000),
                fontSize: 20,
                fontWeight: FontWeight.w700
              )
            ),

            Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [

                  Container(
                    margin : const EdgeInsets.only(bottom : 10),
                    child: Text(
                      "SNS로 시작하기",
                      style : TextStyle(
                        color : Colors.grey,
                        fontSize: 14.sp,
                        fontWeight: FontWeight.w600
                      )
                    ),
                  ),


                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: [
                      GestureDetector(
                        onTap: () {
                          signInApple(context);
                        },
                        child: Image.asset(
                          "assets/images/auth/apple_signin.png",
                          width : 42.sp,
                          height : 42.sp,
                          fit: BoxFit.fitWidth,
                        ),
                      ),
                  
                      SizedBox(width: 20.sp,),
                  
                      GestureDetector(
                        onTap: () {
                          signInGoogle(context);
                        },
                        child: Image.asset(
                          "assets/images/auth/google_signin.png",
                          width : 42.sp,
                          height : 42.sp,
                          fit: BoxFit.fitWidth,
                        ),
                      )
                    ],
                  ),
                ],
              ),
            )
          ],
        ),
      ),
    );
  }  
}