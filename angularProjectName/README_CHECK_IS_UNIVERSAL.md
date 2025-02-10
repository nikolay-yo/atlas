To check if `@nguniversal/express-engine` is installed in your project, you can follow these steps:

1. **Check `package.json`:**
   - Open your project folder.
   - Look at the `package.json` file.
   - Under the `dependencies` or `devDependencies` section, search for `@nguniversal/express-engine`.

   It should look something like this:

   ```json
   "dependencies": {
     "@nguniversal/express-engine": "^latest_version",
     ...
   }
   ```

2. **Use npm or yarn command:**
   You can also run the following command in the terminal from your project directory to check if `@nguniversal/express-engine` is installed:

   - Using npm:

     ```bash
     npm list @nguniversal/express-engine
     ```

   - Using yarn:

     ```bash
     yarn list @nguniversal/express-engine
     ```

   If it's installed, the command will show the installed version of `@nguniversal/express-engine`. If it's not installed, you will get a message saying it is not found.

Let me know if you need further assistance!

Server Side Rendering
SSR angular app, how to detect if there is loading on server

In an Angular Universal (SSR) application, detecting if the app is running on the **server** or **client** is a common need. You might want to conditionally execute certain code on the server or client, for example, when checking if a resource or component is being loaded in the server-side rendering (SSR) context.

Angular Universal runs the app on the server during the initial page load and then hands it over to the client for subsequent interactions. To handle this, you can use Angular's **`isPlatformBrowser`** and **`isPlatformServer`** functions to detect if your code is running on the client or server.

### Steps to Detect if Running on the Server (SSR):

1. **Import Angular's Platform Detection:**
   - To detect the platform (server or browser), Angular provides `PLATFORM_ID` and the helper functions `isPlatformBrowser` and `isPlatformServer` from the `@angular/common` package.

2. **Use `isPlatformServer` to Detect Server-side Rendering:**
   - On the server, `window` and `document` are not available. By using `isPlatformServer`, you can check if the code is being executed in the SSR (server-side) context.

3. **Use `isPlatformBrowser` to Detect Browser Context:**
   - On the client-side (browser), you can check if the code is running in the browser using `isPlatformBrowser`.

### Example Implementation:

#### 1. Install Angular Universal (if not already):
If you haven’t set up Angular Universal yet, you can add it using the Angular CLI:

```bash
ng add @nguniversal/express-engine
```

#### 2. Example Service to Detect Server/Client:

```typescript
import { Injectable } from '@angular/core';
import { isPlatformServer, isPlatformBrowser } from '@angular/common';
import { PLATFORM_ID, Inject } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class PlatformService {

  constructor(@Inject(PLATFORM_ID) private platformId: Object) {}

  // Method to detect if the code is running on the server
  isServer(): boolean {
    return isPlatformServer(this.platformId);
  }

  // Method to detect if the code is running on the client (browser)
  isBrowser(): boolean {
    return isPlatformBrowser(this.platformId);
  }
}
```

#### 3. Use in Component:

In your component, you can inject the `PlatformService` and use the `isServer()` and `isBrowser()` methods to detect the platform.

```typescript
import { Component, OnInit } from '@angular/core';
import { PlatformService } from './platform.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {

  isLoadingOnServer: boolean = false;

  constructor(private platformService: PlatformService) {}

  ngOnInit(): void {
    if (this.platformService.isServer()) {
      // Perform logic for server-side rendering (SSR)
      this.isLoadingOnServer = true;
      console.log('Running on the server');
    } else if (this.platformService.isBrowser()) {
    this.isLoadingOnServer = true;
      // Perform logic for client-side rendering
      console.log('Running in the browser');
    }
  }
}
```

### Explanation:

1. **`PLATFORM_ID` Injection:**
   - `PLATFORM_ID` is injected into the service to detect the platform where the code is running. This is provided by Angular's `@angular/core` module and used with `isPlatformServer` and `isPlatformBrowser`.

2. **`isPlatformServer` and `isPlatformBrowser`:**
   - `isPlatformServer`: Returns `true` if the app is running in an SSR (server-side rendering) context.
   - `isPlatformBrowser`: Returns `true` if the app is running in a browser context.

3. **Component Use:**
   - The component uses the `PlatformService` to check whether the app is running on the server or the browser and performs different logic accordingly.

### Server-Side vs Client-Side Logic:
- **On the server**: When running SSR (on the server), the app will typically render HTML and send it to the browser. This is where you might want to detect loading states or handle server-side operations.
- **On the client**: Once the page is loaded in the browser, the client-side Angular app takes over. This is where you might interact with `window` or `document`.

### Example for Conditional Rendering:

In Angular Universal, sometimes you need to ensure that certain DOM-dependent logic only runs in the client and not during SSR. For example, detecting the window size:

```typescript
ngOnInit() {
  if (this.platformService.isBrowser()) {
    // Only run on the client-side
    window.addEventListener('resize', this.onResize);
  }
}
```

### Important Notes:
- **Server-side rendering (SSR)** means that Angular runs the application on the server first, rendering HTML and sending it to the client, which is then hydrated into a client-side Angular app.
- **Client-side rendering (CSR)** happens after the initial SSR page is loaded, where Angular takes over on the client side and updates the DOM.

### Conclusion:
By using `isPlatformServer` and `isPlatformBrowser`, you can easily detect and handle logic based on the environment (server or client) in Angular Universal. This allows you to avoid accessing browser-specific objects (`window`, `document`) during SSR and ensures the correct execution environment for your app.

Let me know if you need further details or assistance!