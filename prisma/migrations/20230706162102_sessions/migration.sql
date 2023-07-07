-- CreateTable
CREATE TABLE "sessions" (
    "id" SERIAL NOT NULL,
    "uid" TEXT NOT NULL,
    "session" TEXT NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "expires_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "sessions_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "sessions_session_key" ON "sessions"("session");
