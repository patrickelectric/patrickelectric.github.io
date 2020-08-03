+++
title = 'QML Online - Can be everywhere!'
date = 2020-08-03T18:59:39z
[taxonomies]
tags = [ "kde", "qml", "qt", "webasm", "web", "internet" ]
[extra]
header = "/assets/qmlonline_everywhere/code.png"
+++

A new feature of QML Online is already available, allows it to run in any site/blog with minimal js/html code!

Hopefully, our experience with QML examples, tutorials and documentation should change in the near future.

<!-- more -->

Ff you don't know what [QML Online](https://qmlonline.kde.org/) is, please take a look in my previous posts:
 - [QML Online - First version](../qmlonline-first-version)
 - [QML Online - QML Online - A new home!](../qmlonline-a-new-home)

# What are we talking about ?

QML Online now can be used in any blog or website without much work, like this:

<script type="text/javascript" src="https://qmlonline.kde.org/qtloader.js"></script>
<script type="text/javascript" src="https://qmlonline.kde.org/qml.js"></script>

{% qmlonline(name="qmlonline") %}
import QtQuick 2.7
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.12

Rectangle {
    color: "#179AF3"
    anchors.fill: parent

     ColumnLayout{
        anchors.bottom: parent.bottom
        anchors.right: parent.right
        CheckBox {
            checked: true
            text: "Check this!"
        }
        CheckBox {
            text: "Or this!"
        }
    }

    Text {
        text: "KDE"
        font.pixelSize: 80
        font.bold: true
        color: "#82CB38"
        anchors.centerIn: parent
        RotationAnimator on rotation {
            running: true
            loops: Animation.Infinite
            from: 0
            to: 360
            duration: 1500
        }
    }
}
{% end %}

And how can this new feature be used ?

It's quite simple, check this minimal HTML example:

```html
<html>
<head>
    <title>Qml Online minimal example</title>
</head>
<body>
    <script type="text/javascript" src="https://qmlonline.kde.org/qtloader.js"></script>
    <script type="text/javascript" src="https://qmlonline.kde.org/qml.js"></script>

    <div id="qmlonline"></div>

    <script type='text/javascript'>
        const qml = new QmlOnline("qmlonline")
        qml.registerCall({
            qmlMessage: function(msg) {
                console.log(`qml message: ${msg}`)
            },
            qmlError: function(data) {
                console.log(`qml error: ${JSON.stringify(data)}`)
            },
            posInit: function() {
                qml.setCode(`
                    import QtQuick 2.7
                    import QtQuick.Controls 2.3
                    Rectangle {
                        color: "#179AF3"
                        anchors.fill: parent
                        Text {
                            text: "KDE"
                            font.pixelSize: 80
                            font.bold: true
                            color: "#82CB38"
                            anchors.centerIn: parent
                            RotationAnimator on rotation {
                                running: true
                                loops: Animation.Infinite
                                from: 0
                                to: 360
                                duration: 1500
                            }
                        }
                    }
                `)
            },
        })
        qml.init()
    </script>
</body>
</html>
```

As you can see, there is three steps, include both `qtloader.js` and `qml.js`, add a `div` DOM and create a `QmlOnline` object.
Since I'm not a web expert, probably there is a better way to organize this approach for the user and bugs may exist.
Be free to create [Merge Requests](https://invent.kde.org/webapps/qmlonline/-/merge_requests), or get in touch with [feature requests and issues](https://invent.kde.org/webapps/qmlonline/-/issues/new).

# What is next ?

From my planned objectives, sharing QML Online as library to be available for any website was one of the final points, the only one that's still missing is the Kirigami support, that's still in progress and hopefully will be finished until the end of the year (if everything goes fine).

There is also a small bug, where [it's not possible to use multiple QML Online instances on the same webpage](https://invent.kde.org/webapps/qmlonline/-/issues/3).