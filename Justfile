dev:
    poetry run uvicorn auth.main:app --reload --host "0.0.0.0" --port 3000

serve:
    poetry run uvicorn auth.main:app --host "0.0.0.0" --port 3000

lint:
    poetry run ruff check .

format:
    poetry run ruff . --fix
    poetry run black .

migrate arg:
    #!/usr/bin/env zsh
    case {{arg}} in
        "dev")
            poetry run prisma migrate dev
            poetry run prisma generate
            ;;
        "deploy")
            poetry run prisma migrate deploy
            ;;
        *)
            echo "Invalid argument"
            ;;
    esac

migrate-dev:
    poetry run prisma migrate dev
    poetry run prisma generate

clean:
    fd -I __pycache__ -x rm -rf
