{
    "targets": [
        {
            "target_name": "po-addon",
            "sources": [
                "./addons/src/po_addon_interface.cpp",
                "./addons/third_party/libinjection/src/libinjection_xss.c",
                "./addons/third_party/libinjection/src/libinjection_sqli.c",
                "./addons/third_party/libinjection/src/libinjection_html5.c"
            ],
            "include_dirs": [
                "<!@(node -p \"require('node-addon-api').include\")",
                "./addons/third_party/libinjection/src/"
            ],
            "libraries": [
                "<!(echo $PROTECTONCE_LIBNODE)"
            ],
            'defines': ['NAPI_DISABLE_CPP_EXCEPTIONS'],
        },
        {
            "target_name": "po-openrasp-addon",
            "cflags_cc!": ["-fno-exceptions"],
            "cflags_cc+": ["-Wno-unused-variable"],
            "cflags+": ["-Wno-unused-function"],
            "sources": [
                "./addons/src/po_open_rasp_addon.cpp",
                "./addons/third_party/openrasp/openrasp-v8/base/flex/flex.cc"
            ],
            "include_dirs": [
                "<!@(node -p \"require('node-addon-api').include\")",
                "./addons/third_party/openrasp/openrasp-v8/base/flex/"
            ],
            "libraries": [
                "<!(echo $PROTECTONCE_LIBNODE)"
            ],
            'defines': ['NAPI_DISABLE_CPP_EXCEPTIONS'],
        }
    ]
}
