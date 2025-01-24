# Flutter Wear Plugin

A plugin that offers Flutter support for Wear OS by Google (Android Wear).

__To use this plugin you must set your `minSdkVersion` to `23`.__


# Tutorial

https://medium.com/flutter-community/flutter-building-wearos-app-fedf0f06d1b4


# Widgets

There currently three widgets provided by the plugin:

* WatchShape: determines whether the watch is square or round.
* AmbientMode: builder that provides what mode the watch is in. The widget will rebuild whenever the watch changes mode.


## Setup

If you are creating a standalone watch app, add the following to your manifest:

```xml
<application>
  <meta-data
    android:name="com.google.android.wearable.standalone"
    android:value="true"
    />
</application>
```

## Example

```dart
class WatchScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return WatchShape(
      builder: (BuildContext context, WearShape shape, Widget? child) {
        return AmbientMode(
          builder: (context, mode, child) {
            return mode == Mode.active ? ActiveWatchFace() : AmbientWatchFace();
          },
        );
      },
    );
  }
}
```
