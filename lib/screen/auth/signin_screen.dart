import 'dart:convert';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:google_sign_in/google_sign_in.dart';
import 'package:sign_in_with_apple/sign_in_with_apple.dart';

import 'package:http/http.dart' as http;


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
      return;
    } catch (e) {
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
        return;
      } catch (e) {
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

            Column(
              mainAxisAlignment: MainAxisAlignment.end,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Image.asset(
                  "assets/images/auth/apple_signin.png",
                  width : MediaQuery.of(context).size.width - 120,
                  fit: BoxFit.fitWidth,
                ),

                const SizedBox(height: 20,),

                Image.asset(
                  "assets/images/auth/google_signin.png",
                  width : MediaQuery.of(context).size.width - 120,
                  fit: BoxFit.fitWidth,
                )
              ],
            )
          ],
        ),
      ),
    );
  }  
}