# How to Build a Connector on Stacksync Workflows

In this tutorial, we'll guide you through creating connectors on the Stacksy Workflows platform using the Developer Studio. By following these steps, you'll set up your own private app and prepare it for integration.

## Getting Started with Developer Studio

**Step 1:** Navigate to the **Developer Studio** option located under the Workflow Automation menu to access the Private Application Dashboard. Here, you'll begin creating your first private app.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/6335a4f4-c53c-43d5-b166-7744f2305a0a.png)

**Step 2:** Enter the API URL for your application to proceed.

**Step 3:** Access the app connector template, which you can find in our GitHub repo or within our documentation.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/a28c8c83-850e-4c04-95d9-7134493d38d0.png)

**Step 4:** Fork the template to start setting up your connector. This allows you to choose a name for your new repository.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/fd1651dc-6076-41a2-91d9-7c91ae9188af.png)

**Step 5:** Name your new repo, for example, "example workforce App example," and create the fork.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/66ee8d0b-0188-4634-9d33-cd972edbf7b0.png)

**Step 6:** After creating your new repo, proceed to the code SSH section and click **copy** to copy the URL.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/a84f9ee2-f959-444b-aac4-b6714ba41b3f.png)

**Step 7:** Open your preferred IDE, paste the URL, and execute the \`git clone\` command to clone the repository into your local workspace.

**Step 8:** Navigate into your cloned repository by typing \`CD workflow app example\` in your terminal.

**Step 9:** Run the development environment script by entering \`./run_dev.sh\` in your terminal. The command varies slightly depending on your operating system; use \`.bat\` for Windows and \`.sh\` for Mac.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/a5f5ad09-8eed-4296-8a72-03565c266ace.png)

**Step 10:** To make your connector accessible over the Internet, use **ngrok** to expose your local server with a public URL. This step is crucial as it allows the Stacksy platform to discover and utilize your connector.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/ab7c84eb-1ccc-430e-bb77-531c6bcac009.png)

By following these steps, you've successfully set up and exposed your connector, making it ready for use on the Stacksy Workflows platform.

## Setting Up ngrok for Public Access

**Step 1:** Set up ngrok, the tool you'll use for this process.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/1a38e27e-1cce-4a59-9fc4-a93de97676f9.png)

**Step 2:** Visit **ngrok.com** and follow the installation instructions that match your local machine's configuration.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/01c7eacf-42e2-417d-9c37-d2ee2bb9abe4.png)

**Step 3:** Once ngrok is installed, return to your IDE.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/832674b0-7881-4b7b-8da5-7f8c90e2cee8.png)

**Step 4:** Open a new terminal within your IDE.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/25cd9151-1e2d-488d-a5db-2291547ec83b.png)

**Step 5:** Run the command \`ngrok HTTP 2003\`, using the port number specified in your appconfig YAML file.

**Step 6:** Ngrok will then generate a URL that points to your local backend. Click **copy** to copy this URL.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/9bf68b66-1ebd-4a68-bfd1-bec68383e46e.png)

**Step 7:** Paste the copied URL into your browser and click **Visit Site** to ensure everything is running smoothly.

**Step 8:** Take the URL, return to Connector Studio, and paste it there.

**Step 9:** Click **Create** to create your first connector.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/19f0804f-87d5-4255-bd6b-a7027235718f.png)

**Step 10:** Now that you've created your first connector, it's time to use it in a workspace.

## Using Your Connector in a Workflow

**Step 1:** Use the connector in a workflow. Navigate to the **workflow section**.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/0329c5de-3885-48b2-9f14-90e70b5f539b.png)

**Step 2:** Create a new workflow in the same region as the connector you've just created.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/6473c23e-b678-4462-886a-1d5ca0dd7269.png)

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/82d88452-04b0-4b5f-921c-b63dd6757ba4.png)

**Step 3:** Click **Save** to save your newly created workflow.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/96d8d13b-39b0-40ca-9f46-df6132919674.png)

**Step 4:** You now have your workflow set up. Click **Create Action** and scroll to find the **Connector Example app**.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/69418019-6be5-4ce9-84af-6a38528becad.png)

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/7ad12279-c730-4c8c-b892-501b2508e43d.png)

**Step 5:** Click any of the two modules displayed on your screen.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/434f71ee-1b09-4402-b314-633df6998e7d.png)

**Step 6:** Click **Create Contacts** to fetch the form from your local machine and load it onto the UI.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/d9c16f9c-2cda-4d66-9c79-c505e66c5599.png)

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/d9d60236-7c32-47f2-a383-a2cc61e7d29a.png)

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/dcd4425a-652c-4384-a349-9ffddc4db07b.png)

**Step 7:** Select a CRM connection; for instance, search for Salesforce and choose a contact type. You may adjust additional settings as needed, but for this example, we'll leave the default settings.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/8cba6d5a-de60-4615-8dd1-24d0fdd149b1.png)

**Step 8:** Click **Save**.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/c1ad03ad-ea20-4746-a072-0ae83140719b.png)

**Step 9:** Click **Run** to execute your workflow. Check the workflow execution log to see a new log entry which displays the details of the execution, including the input sent and any metadata.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/b8633bcb-3b72-44c4-b6d8-f4a922d1f3c2.png)

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/d2567aa5-5089-4bcd-a0b1-09fc2eb9f57a.png)

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/ce40df40-155d-4403-93b2-e0cffec023fa.png)

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/79ddf989-617c-49e1-bdb7-6f22be2ac486.png)

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/29c1d185-d815-476c-afaa-1434894dd880.png)

## Creating a Custom Action

**Step 1:** To create a new action, navigate to the Source and Routes folder, and copy the new empty action template into Routes. Remove the v2 folder if present, as it's not needed at this moment.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/dd0ca676-8768-4ebe-8ad5-a8547f129beb.png)

**Step 2:** Rename your folder from 'new empty Action' to 'Get Posts' to reflect the new action that retrieves posts from social media.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/c027cbc4-e81e-46d6-a54b-55ccd74ae0b9.png)

**Step 3:** Configure your module by entering a module name and description, such as "GET posts."

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/04a41b23-08f7-4cc9-97a7-17f4fb60298b.png)

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/08695757-c360-48f3-a932-c48dc4abf5ae.png)

## Defining Schema and Routing

**Step 1:** Define the schema that will appear on the UI for user input. Start by specifying the API key required for the API service you are using. This key is essential for authentication and interaction with the API.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/a8bf8a21-810a-4aba-b8ac-e0b4cb29555a.png)

**Step 2:** After defining the API key, specify the platform you are integrating with, such as LinkedIn, and the type of post you want to create, which could be a normal post or a video.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/2ab2c54e-ecc2-4d97-b800-2fcca1fda7ef.png)

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/c68832db-8d6e-46a7-99ec-33297518d2d6.png)

**Step 3:** Ensure the JSON schema is correct by checking that the schema JSON file turns green, indicating all settings are correctly configured.

**Step 4:** Proceed to define the routing in Python, which includes specifying the endpoint \`/execute\`. This endpoint is triggered when the "Run" button is clicked in a workflow that includes this action.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/07b4ba86-1420-4296-951a-80a0a675db7a.png)

**Step 5:** Within the Python route, wrap the request in the request class and include the data object. This object will contain the form data provided by the user.

**Step 6:** Retrieve the necessary data using \`data.get\` and specify the key name required. Add the API key to the headers under an authorization parameter, typically structured as "Authorization: API Key".

**Step 7:** Set up conditional logic for different platforms. For instance, if the platform is Instagram, specify a different URL. For simplicity, use a dummy API URL that remains constant across all cases, setting it within the URL variable.

## Making API Requests and Handling Responses

**Step 1:** Customize your settings based on your needs and then proceed to gather your data.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/fa838291-2c40-4a5d-aabb-403251e7e645.png)

**Step 2:** Execute the following code to make a request and retrieve the data:

\`\`\`

response = request.get(URL, headers)

\`\`\`

Then, extract the JSON response from the retrieved data.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/65b4dc34-eeae-456c-a05c-f80f51b6799b.png)

**Step 3:** Import the **requests** package, which is necessary for making HTTP requests. Ensure you include this package in your \`requirements.txt\` file.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/d3f4dfb0-02b5-437b-8be1-af7be95946bc.png)

**Step 4:** Use the \`response\` object in the data payload of your output. Always utilize the response class provided in the template, filling the data and metadata appropriately with your output and any additional information.

**Step 5:** Save your changes and return to the workflows page to reload your workflow.

**Step 6:** Create a new action by clicking on **Create Action** and scroll to the **Connector Example App**. You will see a new module named "Get Post" that you just created.

**Step 7:** Test the new "Get Posts" action. Reload the workflows page, click on **Create Action**, and scroll to connect to your example app.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/43341fab-b992-4aae-91fb-bfeb1d6d6d2b.png)

**Step 8:** Click on **Get Posts** to automatically load the form from your backend, which includes fields like API key, platform, and post type, as defined in your schema.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/43600010-fe1d-4757-965c-929c7046a844.png)

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/8d61c8db-a6e3-4ec6-9218-41b8f3d5aab6.png)

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/627bb20e-e479-4b99-9cd1-52a7dc62c5e7.png)

**Step 9:** Enter a random API key, select the platform and post type, then save your settings.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/62e6b00b-5a86-412f-9a23-23c73db97654.png)

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/ca4e62bb-c433-44cd-83b5-f2fc35b1c83f.png)

**Step 10:** Run the action. A new execution log will be created, processing your action and fetching posts with the provided API key and other information.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/ed81e4d1-dbb2-4b5c-8a9c-866bd8ea3b7d.png)

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/567d7e84-a5b8-4fca-9d55-efdcc755e60f.png)

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/09de926a-0731-411a-837e-89ba14a0b76c.png)

## Adding Dynamic Fields

**Step 1:** Add a new field to obtain dynamic data. Begin by adding a field named **Users ID User**.

**Step 2:** Specify the type of data for the new field. Do not type "string" but set the label for the field.

**Step 3:** Define the validation for the **Users ID User** field by marking it as required.

**Step 4:** Prepare to specify choices for the field. At this point, add an option called **choices**.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/cce9424a-3461-4964-9ebd-2d7759ca1f12.png)

**Step 5:** Inside the **choices** option, add a parameter called **values**. Keep this list empty as it will be dynamically filled later.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/76660c5d-8c41-4d48-90d0-3e6726c4031d.png)

**Step 6:** Add a new keyword called **content** to handle dynamic data loading.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/469c18df-1641-42a3-a5e1-3bc3c351a37c.png)

**Step 7:** Inside the **content** field, specify the type of content to manage dynamic data loading.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/1250c319-45c1-4665-8769-ec47717214a3.png)

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/5b49259c-8c4a-494a-b3b9-08e1101da456.png)

**Step 8:** Add **content objects** to the configuration. These objects should include an ID for users, allowing dynamic interaction with user data.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/5976089f-66f7-47ab-becd-ef2374ff4436.png)

**Step 9:** Select the appropriate UI widget to display the dynamic choices effectively. Opt for a dropdown menu by setting the **widget** option to **Select Widget** in PascalCase.

## Setting Up Dynamic Data Loading

**Step 1:** Add the user data under the "get user" section within your route. Check the setup in the following screenshot.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/3f4d111e-2833-4b57-99e8-e8e6a3c24bf9.png)

**Step 2:** Insert the user data into your content at the designated point as shown below.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/8a61f918-230d-4ebb-996f-fba92ed98bf1.png)

**Step 3:** Update your route to include the new user field by integrating it where data is being gathered. This change allows the addition of the new route.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/554d6602-bc1d-41b7-84cd-f327c6685599.png)

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/87580d14-8234-4cf3-b92b-e450c1c08962.png)

**Step 4:** Implement the new user field inside your schema. To fetch data for the UI, use the "content endpoint" located in route.py.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/514de608-457e-4630-9488-96bc78da0e16.png)

**Step 5:** Navigate to the content endpoint to observe how it populates the choices in the dynamic fields of the form.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/3af9eb62-1f37-4f4a-9f79-b1507a2a9780.png)

**Step 6:** Under 'data', you'll find 'form data', which includes all fields defined in your schema, and 'content object names'.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/4d7e2d48-6292-4184-af9b-644fe18d7486.png)

**Step 7:** Since you've defined 'users' as the content object name in your schema, expect the endpoint to return a JSON containing 'content object names' and 'ID users'.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/e7522536-6ef6-471f-b0c5-6f74ab422403.png)

**Step 8:** After performing basic validation checks to ensure the uniqueness of 'content object names', add 'users' as your content object name.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/c56106d4-18a3-4f41-b757-e374841644e4.png)

**Step 9:** To dynamically fetch data, access the 'users' endpoint and request user data. Remember to format the user data appropriately.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/7fe341e9-3b31-492b-96b8-97eb084bdd38.png)

## Formatting Dynamic Data

It's crucial to format our user data in a consistent format to ensure proper handling in our application. We'll focus on utilizing the 'format value' and 'label' to manage how data appears and interacts within our system.

**Step 1:** Identify the 'format value' and 'label' for the data. The 'format value' typically represents a unique identifier, such as a user ID, while the 'label' is a more readable format, like the user's first and last name.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/f1d4ad1d-39aa-471b-ac7d-59d3980178f8.png)

**Step 2:** Examine your current data structure to understand what information is available and how it's formatted. This step involves checking the user IDs and usernames.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/cc4ff1be-307d-4791-96ee-07e3465d9157.png)

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/1ce7a16b-860f-4083-affc-ca6d54896e8b.png)

**Step 3:** Configure your data selection. Choose 'ID' as your 'format value' and 'username' as your 'label'. This selection is crucial for ensuring that the data interacts correctly with your endpoint.

**Step 4:** Remove any unnecessary data objects from your configuration. This step helps streamline the data processing and improves efficiency.

**Step 5:** Append the configured data to your content objects. Ensure the 'content object name' matches the previously used name, and include the newly configured data.

**Step 6:** Save your configurations and refresh your module focus. This step is necessary to apply the changes and to see the newly configured user data in action.

**Step 7:** Test the dynamic form field by navigating back to the 'get posts' function. This action triggers a new schema load from your backend, reflecting the updated user options.

By following these steps, you ensure that your application dynamically fetches and displays user data correctly, enhancing both backend functionality and frontend user experience.

## Testing Your Dynamic Form Field

**Step 1:** Select the desired options then click **Save**.

**Step 2:** Confirm that all selections are correct. If you've made a mistake, correct it at this point.

**Step 3:** To test your new dynamic form field, click **Get Posts**. Scroll down to locate the **User** option and select it.

**Step 4:** After selecting the **User** option, verify that all necessary configurations are set to proceed with testing the dynamic form field.

**Step 5:** Repeat the process by clicking **Get Posts** again to reload the dynamic form UI.

**Step 6:** Select the **User** option once more to ensure the form is functioning as expected.

**Step 7:** Observe the dynamic loading of the content.

**Step 8:** To refresh and load all users available in the API, click **Refresh**.

**Step 9:** After refreshing, click **Save** to preserve your settings.

**Step 10:** Click **Run** to execute the form with the new settings.

**Step 11:** Review the results to confirm that the new data is correctly retrieved and displayed.

**Step 12:** Finally, integrate the new field into your execution endpoint. Add it in the headers or wherever necessary in your form configuration, then click **Save**.

**Step 13:** To ensure everything is set up correctly, go back and click on the **Get Posts** module.

## Final Testing in Stacksync Workflows

This section will guide you through testing the dynamic form field in the Stack Sync workflows using the get post module.

**Step 1:** Navigate back to the main screen of Stack Sync and click on **Okay** to proceed.

**Step 2:** Click on **Get Posts** to test the dynamic form field in your workflow.

**Step 3:** Return to Stack Sync and click on the module to reload the user interface, incorporating the new dynamic form field.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/4653afc9-87cf-4da6-8c55-3fd1b54cc390.png)

**Step 4:** Click **Refresh** to fetch live data for your module.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/86a5ac2b-7d35-43f7-a1eb-47c966eadeca.png)

**Step 5:** Select any option from the dynamic choices available. The options will update automatically as the API changes, ensuring the form remains dynamic.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/a8eb9bdb-efbc-45e2-8aac-829541d11802.png)

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/1f3e016b-20ed-4f5b-b59f-effdd9b4d9bd.png)

**Step 6:** Save your configuration by clicking **Save**.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/4cb6baa3-1dbc-48ea-9a3d-8f87b6a2d911.png)

**Step 7:** Run the module by clicking **Run** and observe the API creating your new module.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/105105b7-4c6d-4b15-8a57-93cca6d55399.png)

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/08870d0e-5d02-4af6-8fab-74b15c5e753e.png)

**Step 8:** Check the data output to confirm the module is functioning correctly. Look for **User 1**, which indicates the ID of your user.

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/9d02e588-1d3e-4471-a6b3-929bd74d784f.png)

![](https://usercontent.eu.prod.clueso.io/676f2ec9-9eca-49be-b535-f27fe42c37e8/4b1e9d18-6bba-407c-89d1-b0b8e56bd8d0/beaa37fa-8037-40e4-b627-fa5e3e745a5a/images/55344e27-e9b0-43f4-8d25-b8e643f0c021.png)

**Step 9:** To further customize your module, consider adding a schema with a connection field of type connection. This allows for various connection types and management to be integrated into your module.

By following these steps, you'll effectively test and customize your dynamic form field in Stack Sync workflows. The flexibility of adding and managing connection fields enhances the module’s functionality, making it adaptable to various needs.
