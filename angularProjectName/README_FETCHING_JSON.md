https://nipunipremadasa923.medium.com/a-beginners-guide-to-fetching-json-data-using-angular-1574b48592a1

Step 1: Setting Up the Project

Let’s set up our Angular project. If you haven’t already, install the Angular CLI globally, and run the following command on your terminal.

npm install -g @angular/cli
Now, create a new Angular project named “angular-json”.

ng new angular-json
cd angular-json
Step 2: Creating the JSON File

For this example, we’ll use a simple JSON file containing user information. Create a new file named “info.json” in the “src/assets” folder of your Angular project and add the following data.

[
    {
        "userId": 1,
        "firstName": "Amila",
        "lastName": "Perea"
    },
    {
        "userId": 2,
        "firstName": "Kamal",
        "lastName": "Kumara"
    },
    {
        "userId": 3,
        "firstName": "Ama",
        "lastName": "Fernando"
    }
]
This JSON file contains an array of user objects, each with a userId, firstName, and lastName.

Step 3: Creating the Data Service

Now, let’s create a service to fetch the data from our JSON file. Run the following command to generate a new service.

ng generate service data
Open the generated data.service.ts file and replace its contents with the following code:

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DataService {
  private dataUrl = 'assets/info.json';

  constructor(private http: HttpClient) { }

  getData(): Observable<any[]> {
    return this.http.get<any[]>(this.dataUrl);
  }
}
This service uses Angular’s HttpClient to fetch data from our JSON file. The “getData()” method returns an Observable, which allows us to handle the asynchronous nature of HTTP requests. In a simple way, “Observable” is a special type that helps us handle data that might not be available right away.

Step 4: Creating the Component

Let’s create a component named “data” to display our data. Run the following command in the terminal.

ng generate component data
Open the generated “data.component.ts” file and update it as follows.

import { Component, OnInit } from '@angular/core';
import { DataService } from '../data.service';

@Component({
  selector: 'app-data',
  templateUrl: './data.component.html',
  styleUrls: ['./data.component.css']
})
export class DataComponent implements OnInit {
  users: any[] = [];

  constructor(private dataService: DataService) { }

  ngOnInit(): void {
    this.dataService.getData().subscribe(
      data => this.users = data,
      error => console.error('Error fetching data:', error)
    );
  }
}
This component uses our DataService to fetch the data and store the names in a variable called “users”. The “ngOnInit()” function runs when this part of our page is created. It asks for the data and saves it.

Step 5: Displaying the Data

Now, let’s update our component’s template to display the data. Open “data.component.html” and replace its contents with the following code.

<ul>
    <li *ngFor="let user of users">
        {{user.userId}}. {{user.firstName}} {{user.lastName}}
    </li>
</ul>
This template uses Angular’s *ngFor directive to iterate over our users array and display each user's information.

Step 6: Updating the App Module

To use the HttpClient in our application, we need to import the HttpClientModule. Open “app.module.ts” and update it as follows.

import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { DataComponent } from './data/data.component';

@NgModule({
  declarations: [
    AppComponent,
    DataComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
Step 7: Displaying the Component

Finally, let’s display our DataComponent in the main app component. Open “app.component.html” and replace its contents with:

<h1>User List</h1>
<app-data></app-data>
That’s it! 😌

Now run your application with,

ng serve --open
It will automatically open http://localhost:4200 in your browser, and you should see the list of users from your JSON file displayed on the page as shown in the following image.