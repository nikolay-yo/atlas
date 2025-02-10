import { Injectable, Inject } from '@angular/core';
import { PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser, isPlatformServer } from '@angular/common';

@Injectable({
  providedIn: 'root', // This will make the service globally available
})
export class PlatformCheckService {
  constructor(@Inject(PLATFORM_ID) private platformId: object) {}

  // Method to check if running on the browser (client-side)
  isBrowser(): boolean {
    return isPlatformBrowser(this.platformId);
  }

  // Method to check if running on the server-side (Angular Universal)
  isServer(): boolean {
    return isPlatformServer(this.platformId);
  }
}