export default function ClerkLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex h-screen items-center justify-center ">
      <div>{children}</div>
    </div>
  );
}

// Clerk
