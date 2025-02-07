https://www.freecodecamp.org/news/how-to-add-eslint-to-an-angular-application/

To add **ESLint** to an Angular project (either a new or existing project), follow these steps to set it up properly. I'll guide you through the entire process of installing and configuring **ESLint** in Angular.

### 1. **Install ESLint and Required Packages**

1. **Add ESLint to the project**:
   Open a terminal and run the following command to install ESLint and the necessary plugins for Angular.

   ```bash
   ng add @angular-eslint/schematics
   ```

   This command does the following:
   - Installs **`@angular-eslint/schematics`**.
   - Automatically migrates your project from **TSLint** (if it's in use) to **ESLint**.
   - Sets up all required configurations for **ESLint** in the Angular project.

2. If you **manually** want to install ESLint and the required plugins (in case you are not migrating from TSLint), you can run:

   ```bash
   npm install --save-dev eslint @angular-eslint/eslint-plugin @angular-eslint/eslint-plugin-template
   ```

   These packages provide:
   - **ESLint**: The JavaScript/TypeScript linter.
   - **@angular-eslint/eslint-plugin**: Angular-specific ESLint rules.
   - **@angular-eslint/eslint-plugin-template**: Angular template-specific ESLint rules.

### 2. **Migrate from TSLint to ESLint (If Applicable)**

If your Angular project is using **TSLint**, running the `ng add @angular-eslint/schematics` command will automatically remove **TSLint** and migrate your configuration to **ESLint**.

If you want to manually migrate from **TSLint** to **ESLint** (in case you skipped step 1), you can follow these steps:

1. **Uninstall TSLint** (if previously installed):
   ```bash
   npm uninstall tslint
   ```

2. **Install `@angular-eslint/schematics`**:
   ```bash
   ng add @angular-eslint/schematics
   ```

3. **Configure ESLint for your project**. After running the migration, the configuration files (`.eslintrc.json`, etc.) will be generated for your project.

### 3. **ESLint Configuration for Angular**

After installation, you should have an `.eslintrc.json` file in your project. Here's a sample configuration for **TypeScript** and **Angular templates**:

```json
{
  "root": true,
  "ignorePatterns": ["projects/**/*.spec.ts"],
  "overrides": [
    {
      "files": ["*.ts"],
      "parserOptions": {
        "project": ["tsconfig.json"]
      },
      "extends": [
        "plugin:@angular-eslint/recommended",
        "plugin:@typescript-eslint/recommended",
        "eslint:recommended"
      ],
      "rules": {
        // You can customize your linting rules here
        "@typescript-eslint/no-unused-vars": "warn",
        "@typescript-eslint/explicit-module-boundary-types": "off"
      }
    },
    {
      "files": ["*.html"],
      "extends": ["plugin:@angular-eslint/template/recommended"]
    }
  ]
}
```

### Explanation of the Configuration:
- **`plugin:@angular-eslint/recommended`**: Includes the set of recommended ESLint rules for Angular.
- **`plugin:@typescript-eslint/recommended`**: Includes the recommended TypeScript linting rules.
- **`eslint:recommended`**: Includes the default recommended ESLint rules.
- **Custom rules**: You can add specific rules, such as `@typescript-eslint/no-unused-vars` to catch unused variables, or turn off certain rules based on your preferences.

### 4. **Add ESLint to the Build Process (Optional)**

If you want to integrate **ESLint** into your build process (e.g., to run linting on every commit or as part of your build process), you can use **Angular CLI**.

In your `angular.json` file, find the `"lint"` section under the project’s architect section:

```json
"projects": {
  "your-project-name": {
    "architect": {
      "lint": {
        "builder": "@angular-devkit/build-angular:lint",
        "options": {
          "lintFilePatterns": [
            "src/**/*.ts",
            "src/**/*.html"
          ]
        }
      }
    }
  }
}
```

With this configuration, you can run linting with the following command:
```bash
ng lint
```

This will run ESLint on the specified file patterns (in this case, `*.ts` and `*.html` files).

### 5. **Run ESLint**

After setting everything up, you can run ESLint via the terminal. To lint your entire project, run:

```bash
npx eslint . --ext .ts,.html
```

This command will:
- Lint all `.ts` and `.html` files in your project.

To automatically fix fixable issues, use the `--fix` flag:

```bash
npx eslint . --ext .ts,.html --fix
```

### 6. **(Optional) Set Up Prettier for Code Formatting**

If you also want to set up **Prettier** for automatic code formatting alongside ESLint, follow these steps:

1. **Install Prettier and ESLint Prettier plugin**:
   ```bash
   npm install --save-dev prettier eslint-config-prettier eslint-plugin-prettier
   ```

2. **Update `.eslintrc.json` to integrate Prettier**:
   Modify your `.eslintrc.json` to include Prettier's configurations by extending it:

   ```json
   {
     "extends": [
       "plugin:prettier/recommended",
       "plugin:@angular-eslint/recommended",
       "plugin:@typescript-eslint/recommended",
       "eslint:recommended"
     ]
   }
   ```

   This will ensure that **Prettier** rules are applied when you run **ESLint** and automatically format your code.

### 7. **Linting in VS Code**

To enable linting within **Visual Studio Code**:
1. Make sure you have the **ESLint** extension installed in VS Code.
2. The extension will show linting issues directly within the editor, and you can fix them based on your `.eslintrc.json` settings.
3. If you set up Prettier, VS Code can auto-format your code on save as well.

---

### Summary

1. **Install ESLint** and required plugins using `ng add @angular-eslint/schematics`.
2. **Configure ESLint** by editing the `.eslintrc.json` file (you can extend recommended Angular and TypeScript rules).
3. **Run ESLint** using `ng lint` or `npx eslint . --fix`.
4. Optionally, **add Prettier** for automatic code formatting alongside ESLint.

Let me know if you run into any issues or need further assistance!