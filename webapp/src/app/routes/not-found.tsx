import { Link } from "react-router"

import { Button } from "components/ui/button"
import {
  Card,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "components/ui/card"

export default function NotFound() {
  return (
    <div className="flex items-center justify-center h-screen bg-bg">
      <Card className="w-[420px]">
        <CardHeader className="text-center">
          <CardTitle className="lg:text-7xl text-4xl">404</CardTitle>
          <CardDescription>
            An unexpected error occurred
          </CardDescription>
        </CardHeader>
        <CardFooter className="flex justify-center">
          <Button asChild>
            <Link to="/">Go Back</Link>
          </Button>
        </CardFooter>
      </Card>
    </div>
  )
}