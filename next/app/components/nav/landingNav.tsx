import Button from "../core/button";

export default function LandingNav() {
  return (
    <nav className="w-full">
      <div className='flex justify-between max-w-screen-xl m-auto'>
        <div>
          <h1>iHealth</h1>
        </div>
        <div>
          <ul className="flex flex-row">
            <li>
              <a>
                About
              </a>
            </li>
            <li>
              <a>
                Benefits
              </a>
            </li>
            <li>
              <a>
                Questions
              </a>
            </li>
          </ul>
        </div>
        <Button text="Sign In!"/>
      </div>
    </nav>
  );
}