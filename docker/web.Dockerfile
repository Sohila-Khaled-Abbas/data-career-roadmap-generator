FROM node:18-alpine

WORKDIR /app

# Temporarily copy package.json if it exists (for Next.js scaffolding phase)
# Note: Before building, ensure a package.json exists in the web/ directory.
COPY package*.json ./

RUN if [ -f "package.json" ]; then npm install; fi

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
