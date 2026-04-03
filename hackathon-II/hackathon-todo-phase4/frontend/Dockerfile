FROM node:20-alpine AS base

# Install dependencies only when needed
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies for both production and development
RUN npm ci

# Copy source code
COPY . .

# ----------------------------------------------

# Production build stage
FROM base AS builder

# Build the application
RUN npm run build

# ----------------------------------------------

# Production runner stage
FROM node:20-alpine AS runner

# Set working directory
WORKDIR /app

# Set non-root user for security
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

# Copy necessary files from builder stage
COPY --from=builder --chown=nextjs:nodejs /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/package*.json ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./


# Switch to non-root user
USER nextjs

# Set environment variables
ENV NODE_ENV=production

# Expose port
EXPOSE 3000

# Start the application
CMD ["node", "server.js"]