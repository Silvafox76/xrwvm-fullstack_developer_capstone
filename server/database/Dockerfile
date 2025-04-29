# --- base image -------------------------------------------------------------
    FROM node:18.12.1-bullseye-slim

    # --- work dir ---------------------------------------------------------------
    WORKDIR /app
    
    # --- install dependencies ---------------------------------------------------
    COPY package*.json ./
    RUN npm install          # installs express, mongoose, etc.
    
    # --- copy application code --------------------------------------------------
    COPY . .
    
    # --- run --------------------------------------------------------------------
    EXPOSE 3030
    CMD ["node", "app.js"]
    