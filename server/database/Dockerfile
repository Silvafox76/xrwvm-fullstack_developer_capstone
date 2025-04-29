# server/database/Dockerfile
FROM node:18.12.1-bullseye-slim

# 1️⃣  Set a real work directory
WORKDIR /app

# 2️⃣  Copy only package files first (cache friendly)
COPY package*.json ./

# 3️⃣  Install production deps *inside the image*
RUN npm ci --only=production

# 4️⃣  Copy the rest of the source
COPY . .

# 5️⃣  Start the API
CMD ["node", "app.js"]
