import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:one_vision/screen/auth/signin_screen.dart';
import 'firebase_options.dart';

GlobalKey<NavigatorState> navigatorKey = GlobalKey<NavigatorState>();
final RouteObserver<PageRoute> routeObserver = RouteObserver<PageRoute>();

void main() {

  Future<void> initApp() async {
    // await Firebase.initializeApp(
    //   options: DefaultFirebaseOptions.currentPlatform,
    // );
  }

  initApp();
  runApp(const App());
}

class App extends StatefulWidget {
  const App({super.key});

  @override
  State<App> createState() => AppState();
}

class AppState extends State<App> {
  
  @override
  void initState() {
    super.initState();
    
  }

  @override
  Widget build(BuildContext context) {
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

            return const SignInScreen();                
          }
        );
      },
    );
  }
}
