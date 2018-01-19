/**
 * System configuration for Angular samples
 * Adjust as necessary for your application needs.
 */
(function (global) {
  System.config({
    paths: {
      // paths serve as alias
      'npm:': 'node_modules/'
    },
    // map tells the System loader where to look for things
    map: {
      // our app is within the app folder
      app: 'app',

      // angular bundles
      '@angular/core': 'npm:@angular/core/bundles/core.umd.js',
      '@angular/common': 'npm:@angular/common/bundles/common.umd.js',
      '@angular/common/http': 'https://unpkg.com/@angular/common/bundles/common-http.umd.js',
      '@angular/compiler': 'npm:@angular/compiler/bundles/compiler.umd.js',
      '@angular/platform-browser': 'npm:@angular/platform-browser/bundles/platform-browser.umd.js',
      '@angular/platform-browser-dynamic': 'npm:@angular/platform-browser-dynamic/bundles/platform-browser-dynamic.umd.js',
      '@angular/http': 'npm:@angular/http/bundles/http.umd.js',
      '@angular/router': 'npm:@angular/router/bundles/router.umd.js',
      '@angular/forms': 'npm:@angular/forms/bundles/forms.umd.js',

      '@angular/animations': 'npm:@angular/animations/bundles/animations.umd.js',
      '@angular/material': 'npm:@angular/material/bundles/material.umd.js',
      '@angular/animations/browser':'node_modules/@angular/animations/bundles/animations-browser.umd.js',
      '@angular/platform-browser/animations': 'node_modules/@angular/platform-browser/bundles/platform-browser-animations.umd.js',
      
       // CDK Secondary entry points
      '@angular/cdk/a11y': 'https://rawgit.com/angular/cdk-builds/master/bundles/cdk-a11y.umd.js',
      '@angular/cdk/accordion': 'https://rawgit.com/angular/cdk-builds/master/bundles/cdk-accordion.umd.js',
      '@angular/cdk/bidi': 'https://rawgit.com/angular/cdk-builds/master/bundles/cdk-bidi.umd.js',
      '@angular/cdk/coercion': 'https://rawgit.com/angular/cdk-builds/master/bundles/cdk-coercion.umd.js',
      '@angular/cdk/keycodes': 'https://rawgit.com/angular/cdk-builds/master/bundles/cdk-keycodes.umd.js',
      '@angular/cdk/observers': 'https://rawgit.com/angular/cdk-builds/master/bundles/cdk-observers.umd.js',
      '@angular/cdk/platform': 'https://rawgit.com/angular/cdk-builds/master/bundles/cdk-platform.umd.js',
      '@angular/cdk/portal': 'https://rawgit.com/angular/cdk-builds/master/bundles/cdk-portal.umd.js',
      '@angular/cdk/rxjs': 'https://rawgit.com/angular/cdk-builds/master/bundles/cdk-rxjs.umd.js',
      '@angular/cdk/table': 'https://rawgit.com/angular/cdk-builds/master/bundles/cdk-table.umd.js',
      '@angular/cdk/testing': 'https://rawgit.com/angular/cdk-builds/master/bundles/cdk-testing.umd.js',
      '@angular/cdk/overlay': 'https://rawgit.com/angular/cdk-builds/master/bundles/cdk-overlay.umd.js',
      '@angular/cdk/scrolling': 'https://rawgit.com/angular/cdk-builds/master/bundles/cdk-scrolling.umd.js',
      '@angular/cdk/collections': 'https://rawgit.com/angular/cdk-builds/master/bundles/cdk-collections.umd.js',
      '@angular/cdk/stepper': 'https://rawgit.com/angular/cdk-builds/master/bundles/cdk-stepper.umd.js',
      '@angular/cdk/layout': 'https://rawgit.com/angular/cdk-builds/master/bundles/cdk-layout.umd.js',
      
      'tslib': 'https://unpkg.com/tslib@1.7.1',
      // other libraries
      'rxjs':                      'npm:rxjs',
      'angular-in-memory-web-api': 'npm:angular-in-memory-web-api/bundles/in-memory-web-api.umd.js',
      'file-saver':                'npm:file-saver',
      'chart.js':                  'npm:chart.js',
      'hammerjs':                   'npm:hammerjs'
    },
    // packages tells the System loader how to load when no filename and/or no extension
    packages: {
      app: {
        defaultExtension: 'js'
      },
      rxjs: {
        defaultExtension: 'js'
      },
      'file-saver': {
        main: './FileSaver.js',
        defaultExtension: 'js'
      },
      'chart.js':{
        main: '/dist/Chart.bundle.js',
        defaultExtension: 'js'
      },
      'hammerjs':{
        main: './hammer.js',
        defaultExtension: 'js'
      }
    }
  });
})(this);
