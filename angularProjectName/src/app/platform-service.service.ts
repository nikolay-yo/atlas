import { Inject, Injectable, PLATFORM_ID } from '@angular/core';
import { isPlatformServer, isPlatformBrowser } from '@angular/common'

@Injectable({
  providedIn: 'root'
})
export class PlatformServiceService {

  constructor(@Inject(PLATFORM_ID) private platformId: object) { }

  // Method to detect if the code is running on the server
  isServer(): boolean {
    return isPlatformServer(this.platformId);
  }

  // Method to detect if the code is running on the client (browser)
  isBrowser(): boolean {
    return isPlatformBrowser(this.platformId);
  }
}
