-- CreateTable
CREATE TABLE "access_logs" (
    "id" SERIAL NOT NULL,
    "action" TEXT NOT NULL,
    "uid" TEXT NOT NULL,
    "success" BOOLEAN NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "access_logs_pkey" PRIMARY KEY ("id")
);
