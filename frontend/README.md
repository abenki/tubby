# Tubby Frontend

This is the frontend for the **Tubby** project, built with **Vue.js**, **TailwindCSS**, and **DaisyUI**. The frontend communicates with a Python backend to fetch YouTube video details and allow users to download videos from URLs.

## Technologies Used

- **Vue.js**: A progressive JavaScript framework for building user interfaces.
- **TailwindCSS**: A utility-first CSS framework for rapidly building custom designs.
- **DaisyUI**: A component library built on top of TailwindCSS for pre-built UI components.
- **Vite**: A fast, modern build tool for web development, used for bundling the frontend assets.

## Project Structure

```
frontend/
├── public/                # Static files
├── src/                   # Source files for the frontend
│   ├── assets/            # Static assets like images and icons
│   ├── components/        # Vue components used throughout the app
│   ├── App.vue            # Root Vue component
│   ├── main.js            # Main entry file for the Vue app
│   └── style.css          # TailwindCSS / DaisyUI configuration file
├── .gitignore             # Git ignore file
├── index.html             # Entry point for the Vite application
├── package.json           # Node.js dependencies and scripts
├── package-lock.json      # Exact dependency tree for reproducible builds
├── README.md              # Project documentation
└── vite.config.js         # Vite configuration file
```
