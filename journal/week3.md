# Week 3 - Decentralized Authentication (Homework Challenge)

Week 3 focused on Decentralized Authentication, a method of verifying one's identity without relying on a centralized authority. I successfully Installed and configured Amplify client-side library for Amazon Cognito, Implemented API calls to Amazon Cognito for custom login, signup, recovery, and forgot password pages. I integrated functions that showed conditional elements and data based on the user's login or logout pattern. Finally, I implemented JWT Token server-side verification to serve our authenticated API endpoints.

The homework challenge for this week was to explore different methods of integrating the AWS-jwt-verify library and implementing an IDP login option for the Cruddur app.

## Task 1 - Implement an IdP login (using Google and AWS  Cognito)

To implement an IdP login using Google and AWS Cognito, I took these steps:

1. Set up a Google API project and enable the Google Sign-In API.
2. Create an AWS Cognito User Pool and enable Google as an Identity Provider.
3. Configure the Google API project to use the AWS Cognito User Pool as an OAuth 2.0 provider.
4. Integrate the Google Sign-In SDK into your application and authenticate users with the AWS Cognito User Pool.

### Step 1: Set up a Google API project and enable the Google Sign-In API

- Open a new tab on the browser, and navigate to the [**Google Cloud console**](https://console.cloud.google.com/apis/dashboard). Then click **Select a project**.

![google1.png](/_docs/assets/week-3/google1.png)

- Click **New Project**. Enter the unique project name, and click **Create**.

![google2.png](/_docs/assets/week-3/google2.png)

![google3.png](/_docs/assets/week-3/google3.png)

- Next, select **APIs & Services** from the navigation menu on the left-hand side. Then click **OAuth consent screen > c**lick **Create.**
    
    ![google6.png](/_docs/assets/week-3/google6.png)
    

- Fill in the required information for the App Registration, App Information, and Developer Contact Information fields, then click **Save and Continue**. Enter the necessary details on the **OAuth Consent Screen**, **Scopes**, and **Test Users page** to ****finish setting up the consent screen.

![1.png](/_docs/assets/week-3/1.png)

- Next, click the **Credentials** tab. To create the OAuth 2.0 credentials, select **OAuth client ID** from the **Create credentials** dropdown list.

![google7.png](/_docs/assets/week-3/google7.png)

- Next, select **Web application** as the **Application type** and enter the unique name for the **OAuth client**. Then click **Create.**

![3.png](/_docs/assets/week-3/3.png)

- Download a JSON copy of the **Client ID** and **Client Secret** generated. Then click **Ok**.

### Step 2: Create an AWS Cognito User Pool and enable Google as an Identity Provider

- I used an existing user pool called **cruddur-pool**. However, visit [**create a user pool using AWS Cognito](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pool-as-user-directory.html).**
- Choose the **Sign-in Experience** tab. Locate **Federated sign-in** and then select **Add an identity provider**.
- Choose a social IdP: **Google**.

![4a.png](/_docs/assets/week-3/4a.png)

- Based on our choice of social Idp selected. Enter the **App client ID** and **client secret** generated in the previous section.
- Enter the names of the **Authorized scopes** you want to use. Scopes define which user attributes (such as `name` and `email`) you want to access with your app. For Google, enter the following:

| Social identity provider | Example scopes |
| --- | --- |
| Google | profile email openid |
- Map attributes from your IdP to your user pool.

| User pool attribute | Google attribute |
| --- | --- |
| email | email |
| name | name |
| preferred_username | given_name |
| username | sub |
- Next, click **Add identity provider**.

![5.png](/_docs/assets/week-3/5.png)

- From the **App client integration** tab, choose one of the **App clients** in the list and **Edit hosted UI settings**.
    - Add an **Allowed callback URL** ([**http://localhost:3000**](http://localhost:3000/)) and an **Allowed sign-out URL** **(optional).
    - Select **Google** as the **Identity provider** available to the app client.
    - Set the **OAuth 2.0 grant types** to **Implicit Grant**. This specifies that the client should directly receive the access token.
    - Choose an OpenID Connect scope, select **Profile**, **Email**, **OpenID**, and **aws.cognito.signin.user.admin**.
    

![7.png](/_docs/assets/week-3/7.png)

- Click on **Save changes**.

### Step 3: Configure the Google API project to use the AWS Cognito User Pool as an OAuth 2.0 provider

- Go to the [**Google Cloud console**](https://console.cloud.google.com/apis/dashboard). Choose **Credentials** (on the left nav bar).
- Select the client you created in the first step, and click the **edit** button.

![13a.png](/_docs/assets/week-3/13a.png)

- Type your user pool domain into **Authorized Javascript origins.**
- Type your user pool domain with the `/oauth2/idpresponse` endpoint into **Authorized Redirect URIs**.

![google8.png](/_docs/assets/week-3/google8.png)

- Click **Save**.
- Test the social Idp configuration:
    - Navigate back to AWS Cruddur-pool Console.
    - Under the **Domain menu** in the **App Integration** **tab**, click the **Action** dropdown, and select **Create Cognito domain**.
    - Enter a **unique/qualified domain prefix.** Then click **Save**.
    
    ![8.png](/_docs/assets/week-3/8.png)
    
    You can create a login URL using the elements from the previous two sections. Update the given URL below with your credentials and use it to test your social IdP configuration.
    
    - Replace `<your_user_pool_domain>` with the domain URL you just created
    - Replace `<your_client_id>` with the Client ID of your user pool app client setting
    - Replace the **redirect_uri** parameter with your callback URL (`http://localhost:3000`).
    
    ```html
    https://<your_user_pool_domain>/login?response_type=code&client_id=<your_client_id>&redirect_uri=https://www.example.com
    ```
    
    - Upon visiting the URL above, the page below was displayed.
    
    ![9.png](/_docs/assets/week-3/9.png)
    

### Step 4: Integrate the Google Sign-In SDK into your application and authenticate users with the AWS Cognito User Pool.

- **Update App.js file**
    - Add this environment variable below to the `docker-compose.yml` file under the frontend service.
    
    ```jsx
    REACT_APP_FRONTEND_URL: "https://3000-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
    ```
    
    - Update the `frontend-react-js/src/App.js` file.
    
    ```jsx
    Amplify.configure({
      AWS_PROJECT_REGION: process.env.REACT_APP_AWS_PROJECT_REGION,
      aws_cognito_region: process.env.REACT_APP_AWS_COGNITO_REGION,
      aws_user_pools_id: process.env.REACT_APP_AWS_USER_POOLS_ID,
      aws_user_pools_web_client_id: process.env.REACT_APP_CLIENT_ID,
      oauth: { // -- add update here --
        domain: '<your_user_pool_domain_without_http/https>',
        scope: ['email', 'profile', 'openid', "aws.cognito.signin.user.admin"],
        redirectSignIn: process.env.REACT_APP_FRONTEND_URL,
        redirectSignOut: process.env.REACT_APP_FRONTEND_URL,
        responseType: 'token' // a REFRESH token will only be generated when the responseType is code
      },
    
      Auth: {
        // We are not using an Identity Pool
        // identityPoolId: process.env.REACT_APP_IDENTITY_POOL_ID, // REQUIRED - Amazon Cognito Identity Pool ID
        region: process.env.REACT_APP_AWS_PROJECT_REGION, // REQUIRED - Amazon Cognito Region
        userPoolId: process.env.REACT_APP_AWS_USER_POOLS_ID, // OPTIONAL - Amazon Cognito User Pool ID
        userPoolWebClientId: process.env.REACT_APP_CLIENT_ID, // OPTIONAL - Amazon Cognito Web Client ID (26-char alphanumeric string)
      },
    });
    ```
    

- **Automatically set redirect URL in Cognito:** this will set the redirect URL in Cognito Hosted UI settings to be the same as our frontend URL.
    - Create a `/bin` folder in the `frontend-react-js` directory.
    - Create a bash script named `[auto-redirect](http://auto-redirect.sh)` to automatically update the URL whenever we open a workspace in Gitpod.
    - Add the script below:
    
    ```bash
    #! /usr/bin/bash
    
    aws cognito-idp update-user-pool-client \
    --user-pool-id <REACT_APP_AWS_USER_POOLS_ID> \
    --client-id <REACT_APP_CLIENT_ID> \
    --callback-urls https://3000-$GITPOD_WORKSPACE_ID.$GITPOD_WORKSPACE_CLUSTER_HOST \
    --logout-urls https://3000-$GITPOD_WORKSPACE_ID.$GITPOD_WORKSPACE_CLUSTER_HOST \
    --supported-identity-providers Google \
    --allowed-o-auth-flows-user-pool-client \
    --allowed-o-auth-flows implicit \
    --allowed-o-auth-scopes {email, opened, profile,aws.cognito.signin.user.admin}
    ```
    
    - Make the script executable using **chmod u+x** from the root folder.
    - Run this script and verify if you get a valid response. Confirm changes have been made in **cruddur-pool → App Integration → Select App client → Hosted UI**
    - The Hosted UI status should have changed to **Available**, as seen below:
    
    ![12.png](/_docs/assets/week-3/12.png)
    
- **Add Google Sign in button**
    - Update the frontend `pages/SigninPage.css` by adding:
    
    ```css
    @import url(https://fonts.googleapis.com/css?family=Roboto:500);
    
    $white: #fff;
    $google-blue: #4285f4;
    $button-active-blue: #1669F2;
    
    .google-btn {
      width: 204px;
      height: 42px;
      background-color: $google-blue;
      border-radius: 2px;
      box-shadow: 0 3px 4px 0 rgba(0,0,0,.25);
      .google-icon-wrapper {
        position: absolute;
        margin-top: 1px;
        margin-left: 1px;
        width: 40px;
        height: 40px;
        border-radius: 2px;
        background-color: $white;
      }
      .google-icon {
        position: absolute;
        margin-top: 11px;
        margin-left: 11px;
        width: 18px;
        height: 18px;
      }
      .btn-text {
        float: right;
        margin: 11px 11px 0 0;
    		background-color: transparent; 
    	  border: none;
        font-size: 14px;
        letter-spacing: 0.2px;
        font-family: "Roboto";
      }
      &:hover {
        box-shadow: 0 0 6px $google-blue;
      }
      &:active {
        background: $button-active-blue;
      }
    }
    
    .center-a-div {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 300px;
     }
    
    ```
    
    - Update the `pages/SigninPage.js` *by adding:*
    
    ```html
    <div className="center-a-div">
      <div className="google-btn" onClick={() => Auth.federatedSignIn({ provider: 'Google' })}>
        <div className="google-icon-wrapper">
          <img className="google-icon" src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg" />
        </div>
        <p class="btn-text"><b>Continue with google</b></p>
      </div>
    </div>
    ```
    
    - See the result below:
    
    ![10a.png](/_docs/assets/week-3/10a.png)
    

- **Collect Access Token**
    - Update `pages/HomeFeedPage.js` by adding:
    
    ```jsx
    const getIdToken = async () => {
    
        Auth.currentSession().then(res => {
          let accessToken = res.getAccessToken()
    
          localStorage.setItem(
            "access_token",
            accessToken.jwtToken
          );
    
          loadData();
          checkAuth();
    
        })
      }
    ```
    
    - Update React.useEffect to this:
    
    ```jsx
    React.useEffect(() => {
        //prevents double call
        if (dataFetchedRef.current) return;
        dataFetchedRef.current = true;
    
        getIdToken();
    
      }, []);
    ```
    

Finally, run `docker-compose up` to start the application. Click the "Sign in with Google" button to open the Google sign-in page. After signing in, you will be redirected back to the frontend url.

![10.png](/_docs/assets/week-3/10.png)

![11.png](/_docs/assets/week-3/11.png)

![14.png](/_docs/assets/week-3/14.png)

Overall, the homework challenge for Week 3 provided a comprehensive understanding of decentralized authentication systems and their applications. As the need for secure and trustworthy identity verification grows across various industries, decentralized authentication systems are becoming increasingly important. It is crucial that we have a strong understanding of these systems to ensure a more secure and decentralized future.

References & Sources: 

- [**AWS Amplify Doc**](https://docs.amplify.aws/lib/auth/social/q/platform/js/#setup-your-auth-provider)
- [**AWS Amazon Cognito Doc**](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-social-idp.html)
- [**AWS Amazon Cognito Developer Guide**](https://docs.aws.amazon.com/cognito/latest/developerguide/google.html)
- [**AWS Cognito CLI Command Reference**](https://docs.aws.amazon.com/cli/latest/reference/cognito-idp/update-user-pool-client.html)
- [**Stack Overflow**](https://stackoverflow.com/questions/48777321/aws-amplify-authentication-how-to-access-tokens-on-successful-auth-signin)
- [**CodePen.io**](https://codepen.io/stefanjs98/pen/ambVgK)
- [**Dev Community**](https://dev.to/annleefores/cruddur-google-idp-integration-with-aws-cognito-without-hosted-ui-48j0)