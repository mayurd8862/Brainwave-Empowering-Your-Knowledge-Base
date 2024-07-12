# 🧠 BrainWave: 🤖 Empowering Your Knowledge Base

Welcome to **🧠 BrainWave: 🤖 Empowering Your Knowledge Base** – your ultimate companion for project management and data interaction. With Brainwave, you can chat with PDFs and websites, craft insightful notes, and effortlessly summarize documents—all in one place! Upgrade your productivity and streamline your workflow with Brainwave today. 🚀💡


## ✨ Features 
- **📂 Project Management** : Organize your notes and documents project-wise.
- **💬 Chat with Documents** : Interact with your PDFs and websites through an intuitive chat interface.
- **📝 Document Summarization** : Generate concise summaries of your PDF documents.


## 🛠️ Installation 
To get started with BrainWave, follow these steps:

1. **Clone the Repository**
    ```bash
    git clone https://github.com/mayurd8862/Brainwave-Empowering-Your-Knowledge-Base.git
    ```

2. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Application**
    ```bash
    streamlit run 🏠_Home.py
    ```
    
4. **Access the Application in browser**
   ```bash
   http://localhost:<port_no>
   ```

## 🏗️ Architecture

The web application architecture will consist of the following components:

### 1. Frontend Web Application Built Using Streamlit:

- The frontend of the application is developed using Streamlit, a powerful and easy-to-use framework for building data-driven web applications.
- Streamlit allows for rapid prototyping and development, providing an interactive and responsive user interface for the application.

![image](https://github.com/mayurd8862/Brainwave-Empowering-Your-Knowledge-Base/assets/113239727/38ac6223-a0bc-4c3c-99ed-ac8ea335e6f1)

  
### 2. Sign Up, Sign In Option and Forgot Password Along with Email OTP Verification:

- The application features a comprehensive user authentication system.
- New users can sign up by providing necessary details. Existing users can sign in using their credentials.
- In case users forget their password, they can reset it by receiving an OTP on their registered email, ensuring secure and verified access to their accounts.
  
### 3. Save Notes and View Notes of Projects:

- Users have the ability to create, save, and manage notes related to their projects.
- The notes can be categorized and tagged for easy retrieval. This feature helps users keep track of important information, ideas, and progress related to their projects.
- A user-friendly interface is provided to view and organize notes efficiently.
  
### 4. Document Summarization Using Map Reduce Technique:

- The application incorporates a document summarization feature with impactfull emojis using the MapReduce technique.
- This involves breaking down documents into smaller chunks, summarizing each chunk, and then aggregating the summaries to generate a final concise summary.
- This helps users quickly understand the main points and key information from lengthy documents.

![Summarization map-reduce](https://github.com/user-attachments/assets/dccc4bf9-a461-4f4d-a63d-c622c56e3e30)


### 5. Chat with Documents and URLs Using RAG Technique:

- The application includes a feature for users to chat with documents and URLs.
- This is implemented using the RAG (Retrieval-Augmented Generation) technique.
- Users can input queries, and the system retrieves relevant information from the documents and URLs, providing accurate and contextually relevant responses. This enhances the user's ability to extract specific information from large volumes of text.

![RAG Pipeline](https://github.com/user-attachments/assets/9f549bd2-c162-4464-9a3d-41d6919edf69)

   platforms used for:

   - word embedding - all-MiniLM-L6-v2 using langchain_community.embeddings library
   - vector database - facebook's vectorstore 'FAISS'
   - LLM - llama-3-8b using Groq

### 6. Used MongoDB for Storing Notes and Login Credentials:

- MongoDB, a NoSQL database, is used for storing user notes and login credentials.
- MongoDB is known for its scalability, flexibility, and ease of use, making it ideal for managing large volumes of data.
- The database ensures secure storage of user information and provides fast access to notes and authentication data.

### 7. CI/CD Pipeline Using Streamlit Cloud for Automated Deployment:

- The application utilizes a Continuous Integration and Continuous Deployment (CI/CD) pipeline facilitated by Streamlit Cloud. 
- This pipeline automates the process of testing, building, and deploying the application. 
- Any changes made to the codebase are automatically tested and deployed to the live environment, ensuring that the latest updates are always available to users without manual intervention.

## 📜 License 
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 📧 Contact 
For any questions or suggestions, feel free to reach out:

- **Email**: mayur.dabade21@vit.edu
- **GitHub** : [mayurd8862](https://github.com/mayur8862)
- **LinkedIn** : [https://www.linkedin.com/in/mayur-dabade-b527a9230](https://www.linkedin.com/in/mayur-dabade-b527a9230)

---
[Click here](https://brainwave.streamlit.app/) to use the web application.

Thank you for using **🧠 Brainwave: 🤖 Empowering Your Knowledge Base**! We hope it significantly boosts your productivity and makes project management a breeze.

---
