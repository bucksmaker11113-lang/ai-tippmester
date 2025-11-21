import { useRef } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";

export default function HoloRings() {
  const ring1 = useRef();
  const ring2 = useRef();
  const ring3 = useRef();

  useFrame((state) => {
    const t = state.clock.getElapsedTime();
    ring1.current.rotation.z = t * 0.25;
    ring2.current.rotation.z = -t * 0.15;
    ring3.current.rotation.z = t * 0.1;
  });

  const createRing = (args, color, opacity = 0.5) => (
    <mesh>
      <ringGeometry args={args} />
      <meshBasicMaterial
        color={color}
        transparent
        opacity={opacity}
        side={THREE.DoubleSide}
      />
    </mesh>
  );

  return (
    <group rotation={[Math.PI / 2, 0, 0]}>
      <group ref={ring1}>
        {createRing([1.6, 1.7, 128], "#0dd4ff")}
      </group>

      <group ref={ring2}>
        {createRing([2.1, 2.22, 128], "#11cfff")}
      </group>

      <group ref={ring3}>
        {createRing([2.6, 2.75, 128], "#00eaff")}
      </group>
    </group>
  );
}
