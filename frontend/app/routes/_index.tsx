export default function Index() {
  return (
    <div className="p-6 min-h-screen flex items-center justify-center">
      <div className="bg-white shadow-lg rounded-lg p-8 max-w-xl text-center">
        <h1 className="text-6xl font-bold text-[#1E69FC] mb-6 text-left">
          Welcome Jeff, Steph, and Tyler,
        </h1>
        <p className="text-xl font-light mt-4 text-left">
          I&apos;m excited to have the opportunity to interview with Clarium
          Health! Looking forward to discussing how we can collaborate and
          innovate together.
        </p>

        <div className="mt-16">
          <a
            href="/about"
            className="text-blue-500 hover:text-blue-700 transition-colors duration-300 text-lg"
          >
            Learn More About My Work
          </a>
        </div>
      </div>
    </div>
  );
}
