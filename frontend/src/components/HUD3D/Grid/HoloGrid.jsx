import { useRef } from "react";
import { useFrame } from "@react-three/fiber";

export default function HoloGrid() {
  const grid = useRef();

  useFrame((state) => {
    const t = state.clock.getElapsedTime();
    grid.current.material.opacity = 0.35 + Math.sin(t * 1.2) * 0.05;
  });

  return (
    <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -1.2, 0]} ref={grid}>
      <planeGeometry args={[40, 40, 40, 40]} />
      <meshBasicMaterial
        color={"#00eaff"}
        wireframe
        transparent
        opacity={0.35}
      />
    </mesh>
  );
}
