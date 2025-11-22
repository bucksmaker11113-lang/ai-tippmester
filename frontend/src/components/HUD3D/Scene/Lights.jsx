export default function Lights() {
  return (
    <>
      <pointLight position={[0, 3, 3]} color={"#00eaff"} intensity={4} />

      <ambientLight intensity={0.2} color={"#0aa4d4"} />

      <pointLight position={[-3, 2, -2]} intensity={1.5} color={"#11cfff"} />
      <pointLight position={[3, -1, -2]} intensity={1.5} color={"#11cfff"} />
    </>
  );
}
