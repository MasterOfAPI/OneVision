import 'dart:async';
import 'dart:developer';

import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:one_vision/screen/auth/signin_screen.dart';
import 'package:one_vision/screen/home/home.screen.dart';
import 'firebase_options.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

GlobalKey<NavigatorState> navigatorKey = GlobalKey<NavigatorState>();
final RouteObserver<PageRoute> routeObserver = RouteObserver<PageRoute>();

void main() {

  runZonedGuarded(() async {

    WidgetsFlutterBinding.ensureInitialized();

    await Firebase.initializeApp(
        options: DefaultFirebaseOptions.currentPlatform,
    );
    runApp(const App());
  }, 
  (error, stack) { 
    log("앱 실행 에러 : $error");
  });  
}

class App extends StatefulWidget {
  const App({super.key});

  @override
  State<App> createState() => AppState();
}

class AppState extends State<App> {
  
  User? user = FirebaseAuth.instance.currentUser;

  @override
  void initState() {
    super.initState();    
  }

  @override
  Widget build(BuildContext context) {



     return ScreenUtilInit(
        designSize: const Size(360, 800),
        minTextAdapt: true,
        splitScreenMode: true,
        builder : (_, child) {
          return MaterialApp(
            title: 'One Vision',
            navigatorKey: navigatorKey,
            debugShowCheckedModeBanner: false,      
            theme: ThemeData(        
              unselectedWidgetColor: const Color(0xFFFFFFFF),
              bottomSheetTheme: const BottomSheetThemeData(
                backgroundColor: Colors.transparent,
                surfaceTintColor: Colors.transparent,
                shadowColor: Colors.transparent,
              ),
              scrollbarTheme: const ScrollbarThemeData().copyWith(
                mainAxisMargin: 0,
                minThumbLength: 1
              ),
              pageTransitionsTheme: const PageTransitionsTheme(
                builders: {
                  TargetPlatform.android: CupertinoPageTransitionsBuilder(),
                  TargetPlatform.iOS: CupertinoPageTransitionsBuilder(),
                }
              ),
              textSelectionTheme: const TextSelectionThemeData(
                selectionHandleColor: Colors.transparent,
              ),
            ),
            localizationsDelegates: const [
              GlobalMaterialLocalizations.delegate,
              GlobalWidgetsLocalizations.delegate, 
              GlobalCupertinoLocalizations.delegate,
            ],
            supportedLocales: const [
              Locale('en', ''),
              Locale('ko', ''),
            ],          
            navigatorObservers: [
              routeObserver,
            ],
            builder: (context, child) {
              return MediaQuery(
                data: MediaQuery.of(context).copyWith(textScaler: const TextScaler.linear(1.0)),
                child: child!, 
              );
            },
            onGenerateRoute: (settings) {
              return MaterialPageRoute(          
                settings: settings,
                builder: (BuildContext context) {          
                          
                  switch (settings.name) {
                  }
          
                  return const HomeScreen();                
                }
              );
            },
          );
        }
     );
  }
}
