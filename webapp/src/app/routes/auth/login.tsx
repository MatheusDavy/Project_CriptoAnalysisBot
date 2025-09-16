import { Button } from "components/ui/button";
import { Card, CardContent } from "components/ui/card";
import { Input } from "components/ui/input";
import { Label } from "components/ui/label";
import { redirect, useNavigate, type LoaderFunction } from "react-router";
import { authMiddleware } from "middleware/auth";
import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { authenticate } from "http/auth";

export const loader: LoaderFunction = async ({ request }) => {
  return await authMiddleware({ request, type: "public" });
};

export default function Login({}) {
  const navigate = useNavigate();
  const [error, setError] = useState("");

  const { mutate: onAuthenticate, isPending } = useMutation({
    mutationFn: authenticate,
    onSuccess: () => {
      navigate('/dashboard')
    },
    onError: (e) => {
      setError("Erro interno, tente novamente mais tarde!");
    },
  });

  const handleAuthenticate = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const formData = new FormData(event.currentTarget);
    const email = formData.get("email") as string;
    const password = formData.get("password") as string;

    onAuthenticate({ email, password });
  };

  return (
    <div className="bg-fd-muted flex min-h-svh flex-col items-center justify-center p-6 md:p-10">
      <div className="w-full max-w-sm md:max-w-3xl">
        <div className="flex flex-col gap-6 bg-bg">
          <Card className="overflow-hidden p-0">
            <CardContent className="grid p-0 md:grid-cols-2">
              <form
                className="flex flex-col justify-center p-6 md:p-8 min-h-[60vh]"
                onSubmit={handleAuthenticate}
              >
                <div className="flex flex-col gap-6">
                  <div className="flex flex-col items-center text-center">
                    <h1 className="text-2xl font-bold">Bem vindo de volta</h1>
                    <p className="text-muted-foreground text-balance">
                      Veja como estão suas análises
                    </p>
                  </div>
                  <div className="grid gap-3">
                    <Label htmlFor="email">Email</Label>
                    <Input
                      id="email"
                      name="email"
                      type="email"
                      placeholder="m@example.com"
                      required
                    />
                  </div>
                  <div className="grid gap-3">
                    <Label htmlFor="password">Password</Label>
                    <Input
                      id="password"
                      type="password"
                      name="password"
                      placeholder="**********"
                      required
                    />
                  </div>
                  <Button
                    type="submit"
                    variant="accent"
                    className="w-full cursor-pointer"
                    loading={isPending}
                    disabled={isPending}
                  >
                    Login
                  </Button>
                </div>
                {error && (
                  <p className="text-error text-sm text-center mt-10">
                    {error}
                  </p>
                )}
              </form>
              <div className="bg-muted relative hidden md:block">
                <img
                  alt="Image"
                  src="/img/auth/crypto.jpg"
                  className="absolute inset-0 h-full w-full object-cover"
                />
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
