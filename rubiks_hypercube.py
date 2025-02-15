# -*- coding: utf-8 -*-
"""
@author: Daniel Ketterer
"""
import numpy as np

# -------------------------
# Helper functions
# -------------------------

def cat(dim, *arrays):
    """
    to mimic MATLAB's cat(dim, ...) where dim is 1-indexed.
    """
    axis = dim - 1
    new_arrays = []
    for arr in arrays:
        arr = np.array(arr)
        # Ensure the array has at least (axis+1) dimensions:
        if arr.ndim < axis + 1:
            arr = arr.reshape(arr.shape + (1,) * (axis + 1 - arr.ndim))
        new_arrays.append(arr)
    return np.concatenate(new_arrays, axis=axis)

def rotdim(A, k, axes):
    """
    mimic MATLAB's rotdim.
    Rotates array A by 90° k times in the plane defined by axes.
    """
    if A.ndim < 2 or max(axes) >= A.ndim:
        return np.rot90(A, k=k)  # Default to rotation in the (0,1) plane.
    return np.rot90(A, k=k, axes=axes)

def get_int(prompt, min_val=None, max_val=None):
    """
    Prompt the user until a valid integer is entered.
    Optionally enforces a minimum and/or maximum value.
    """
    while True:
        try:
            value = int(input(prompt))
            if min_val is not None and value < min_val:
                print(f"Error: value must be at least {min_val}.")
                continue
            if max_val is not None and value > max_val:
                print(f"Error: value must be at most {max_val}.")
                continue
            return value
        except ValueError:
            print("Error: Invalid input. Please enter an integer.")

# -------------------------
# The Main Computational Functions
# -------------------------

def position(FaceI, s, D, Slice):
    """
    Computes positions
    """
    ###print(f"[DEBUG] position() called with FaceI={FaceI}, s={s}, D={D}, Slice={Slice}")
    y = [0] * D
    y[FaceI - 1] = Slice
    index = 0 if FaceI != 1 else 1
    z = []
    # Change the loop to stop after producing exactly s**(D-2) positions.
    while len(z) < s ** (D - 2):
        ysum = 0
        for n in range(1, D):  # n = 1,...,D-1
            ysum += y[n - 1] * (s ** (n - 1))
        ###print(f"[DEBUG] position() loop: y={y}, index={index}, computed ysum={ysum}")
        z.append(ysum)
        while index < D and y[index] == s - 1:
            ###print(f"[DEBUG] position() inner while: y[{index}] == {s - 1}, resetting y[{index}] to 0")
            y[index] = 0
            if (index + 1) != FaceI:
                index += 1
            else:
                index += 2
            ###print(f"[DEBUG] position() inner while: Updated index={index}, y now {y}")
        if index < D:
            y[index] += 1
            ###print(f"[DEBUG] position(): Incremented y[{index}] to {y[index]}")
            index = 0 if FaceI != 1 else 1
            ###print(f"[DEBUG] position() reset index to {index}")
    ###print(f"[DEBUG] position() returning z: {z}")
    return z

def flip(FaceI, s, D, Slice, FlipAxis):
    """
    Computes the flipped positions as in the MATLAB 'Flip' function.
    """
    ###print(f"[DEBUG] flip() called with FaceI={FaceI}, s={s}, D={D}, Slice={Slice}, FlipAxis={FlipAxis}")
    iter_val = 1
    B = np.array([[1]])
    for i in range(1, D):
        T = B.copy()
        for j in range(1, s):
            B = cat(i, B, T + iter_val)
            iter_val = iter_val + s ** (i - 1)
            ###print(f"[DEBUG] flip() cat loop: i={i}, j={j}, iter_val={iter_val}, B=\n{B}")
    y = [0] * D
    index = 0
    z2 = []
    while index < D - 1:
        ysum = 0
        for n in range(1, D):
            if n != FlipAxis:
                ysum += y[n - 1] * (s ** (n - 1))
            else:
                ysum += ((s - 1) - y[n - 1]) * (s ** (n - 1))
        ###print(f"[DEBUG] flip() loop: y={y}, index={index}, computed ysum={ysum}")
        z2.append(ysum)
        while index < D and y[index] == s - 1:
            ###print(f"[DEBUG] flip() inner while: y[{index}] == {s - 1}, resetting y[{index}] to 0")
            y[index] = 0
            index += 1
            ###print(f"[DEBUG] flip() inner while: Updated index={index}, y now {y}")
        if index < D:
            y[index] += 1
            ###print(f"[DEBUG] flip(): Incremented y[{index}] to {y[index]}")
            index = 0
            ###print(f"[DEBUG] flip() reset index to {index}")
    z2 = [val + 1 for val in z2]  # Adjust for MATLAB's 1-indexing.
    ###print(f"[DEBUG] flip() returning z2: {z2}")
    return z2

def face_move(Face, AxisFrom, AxisTo, Slice, Cube, D, s):
    """
    Performs the face move, similar to MATLAB 'FaceMove'.
    """
    ###print(f"[DEBUG] face_move() called with Face={Face}, AxisFrom={AxisFrom}, AxisTo={AxisTo}, Slice={Slice}, D={D}, s={s}")
    fr = AxisFrom // 2
    to = AxisTo // 2
    if Face < AxisFrom:
        fr = fr - 1
    if Face < AxisTo:
        to = to - 1
    A = Cube[Face - 1].copy()
    ###print(f"[DEBUG] face_move(): Original face (index {Face - 1}) A:\n{A}")
    if A.ndim < 3 or max(fr, to) >= A.ndim:
        ###print(f"[DEBUG] face_move(): Using np.rot90 because condition met (A.ndim={A.ndim}, fr={fr}, to={to})")
        if fr<to:
            A = np.rot90(A, k=-1)
        else:
            A = np.rot90(A, k=1)
    else:
        ###print(f"[DEBUG] face_move(): Using rotdim with k=-1 on axes ({fr}, {to})")
        A = rotdim(A, -1, (fr, to))
    Cube[Face - 1] = A
    ###print(f"[DEBUG] face_move(): Updated Cube face (index {Face - 1}) A:\n{A}")
    return Cube

def other_move(Face, AxisFrom, AxisTo, Slice, Cube, D, s):
    """
    Performs other moves as in MATLAB 'OtherMove'.
    """
    ###print(f"[DEBUG] other_move() called with Face={Face}, AxisFrom={AxisFrom}, AxisTo={AxisTo}, Slice={Slice}, D={D}, s={s}")
    iter_val = 1
    B = np.array([[1]])
    for i in range(1, D - 1):
        T = B.copy()
        for j in range(1, s):
            B = cat(i, B, T + iter_val)
            iter_val = iter_val + s ** (i - 1)
            ###print(f"[DEBUG] other_move() cat loop: i={i}, j={j}, iter_val={iter_val}, B=\n{B}")
    for a in range(1, 2 * D + 1):
        ###print(f"[DEBUG] other_move(): Processing face a={a}")
        fr = AxisFrom // 2
        to = AxisTo // 2
        FaceI = (Face + (Face % 2)) // 2
        if a < AxisFrom:
            fr = fr - 1
        if a < AxisTo:
            to = to - 1
        if a < FaceI:
            FaceI = FaceI - 1
        if (a != AxisFrom and a != AxisTo and a != (AxisFrom - 1)
            and a != (AxisTo - 1) and a != Face):
            if ((Face % 2 == 1 and a != Face + 1) or (Face % 2 == 0 and a != Face - 1)):
                O = Cube[a - 1].copy()
                ###print(f"[DEBUG] other_move(): Original Cube face at index {a-1} O:\n{O}")
                z = position(FaceI, s, D, Slice)
                ###print(f"[DEBUG] other_move(): Computed position z: {z}")
                n_iter = s ** (D - 2) if D - 2 > 0 else 1
                B_sub = np.empty(n_iter, dtype=O.dtype)
                for i_idx in range(n_iter):
                    idx = int(z[i_idx]) - 1
                    ###print(f"[DEBUG] other_move(): a={a}, i_idx={i_idx}, z[i_idx]={z[i_idx]}, computed idx={idx}")
                    B_sub[i_idx] = O.flat[idx]
                    ###print(f"[DEBUG] other_move(): a={a}, i_idx={i_idx}, extracted O.flat[{idx}] = {O.flat[idx]}")
                ###print(f"[DEBUG] other_move(): B_sub before rotation: {B_sub}")
                fr_adj = fr - 1
                to_adj = to - 1
                if B_sub.ndim < 2:
                    B_sub = B_sub.reshape(1, -1)
                    B_rot = np.rot90(B_sub, k=-1).flatten()
                    ###print(f"[DEBUG] other_move(): B_sub reshaped and rotated using np.rot90:\n{B_rot}")
                else:
                    B_rot = rotdim(B_sub, -1, (fr_adj, to_adj))
                    ###print(f"[DEBUG] other_move(): B_sub rotated using rotdim:\n{B_rot}")
                for i_idx in range(n_iter):
                    idx = int(z[i_idx]) - 1
                    O.flat[idx] = B_rot[i_idx]
                    ###print(f"[DEBUG] other_move(): a={a}, i_idx={i_idx}, assigned B_rot[{i_idx}] = {B_rot[i_idx]} to O.flat[{idx}]")
                Cube[a - 1] = O
                ###print(f"[DEBUG] other_move(): Updated Cube face at index {a-1} O:\n{O}")
    return Cube

def axis_move(Face, AxisFrom, AxisTo, Slice, Cube, D, s):
    """
    Performs other moves as in MATLAB 'AxisMove'.
    """
    ###print(f"[DEBUG] axis_move() called with Face={Face}, AxisFrom={AxisFrom}, AxisTo={AxisTo}, Slice={Slice}, D={D}, s={s}")
    iter_val = 1
    FaceI = (Face + (Face % 2)) // 2
    iter_val = 1
    B = np.array([[1]])
    for i in range(1, D - 1):
        T = B.copy()
        for j in range(1, s):
            B = cat(i, B, T + iter_val)
            iter_val = iter_val + s ** (i - 1)
            ###print(f"[DEBUG] axis_move() cat loop: i={i}, j={j}, iter_val={iter_val}, B=\n{B}")
    
    z = position(FaceI, s, D, Slice)
    ###print(f"[DEBUG] axis_move(): Computed position z: {z}")
    
    C = Cube[AxisFrom - 1].copy()
    D1 = Cube[AxisTo - 1].copy()
    E = Cube[AxisFrom - 2].copy()  # Corresponds to MATLAB's Cube{AxisFrom-1}
    F_arr = Cube[AxisTo - 2].copy()
    
    """print(f"[DEBUG] axis_move(): Initial arrays shapes and values:\n"
          f"C (index {AxisFrom-1}):\n{C}\n"
          f"D1 (index {AxisTo-1}):\n{D1}\n"
          f"E (index {AxisFrom-2}):\n{E}\n"
          f"F_arr (index {AxisTo-2}):\n{F_arr}")
    """
    G = C.copy()
    H = D1.copy()
    I_arr = E.copy()
    J = F_arr.copy()
    
    n_iter = s ** (D - 2) if D - 2 > 0 else 1
    
    # Loop 1: Reassign elements among the affected faces.
    for i_idx in range(n_iter):
        idx = int(z[i_idx]) - 1
        ###print(f"[DEBUG] axis_move(): Loop1, i_idx={i_idx}, z[i_idx]={z[i_idx]}, computed idx={idx}")
        G.flat[idx] = F_arr.flat[idx]
        H.flat[idx] = C.flat[idx]
        I_arr.flat[idx] = D1.flat[idx]
        J.flat[idx] = E.flat[idx]
        """print(f"[DEBUG] axis_move(): After assignment at idx={idx}: "
              f"G.flat[{idx}]={G.flat[idx]}, H.flat[{idx}]={H.flat[idx]}, "
              f"I_arr.flat[{idx}]={I_arr.flat[idx]}, J.flat[{idx}]={J.flat[idx]}")
    """
    # Update working copies after loop1.
    C = G.copy()
    D1 = H.copy()
    E = I_arr.copy()
    F_arr = J.copy()
    
    fr = AxisFrom // 2
    to = AxisTo // 2
    if AxisFrom > Face:
        fr = fr - 1
    if AxisTo > Face:
        to = to - 1
    
    # Only perform the second rotation loop for inner moves (i.e. when Slice > 1).
    if Slice > 1:
        z2 = flip(FaceI, s, D - 1, Slice, to - 1)
        ###print(f"[DEBUG] axis_move(): Computed flipped positions z2: {z2}")
        for i_idx in range(n_iter):
            src_idx = int(z[i_idx]) - 1
            pos_index = int(z2[i_idx]) - 1
            ###print(f"[DEBUG] axis_move(): Loop2, i_idx={i_idx}, src_idx={src_idx}, pos_index={pos_index}")
            if pos_index < len(z):
                k = int(z[pos_index]) - 1
                ###print(f"[DEBUG] axis_move(): i_idx={i_idx}, Using pos_index to get k: {k}")
                G.flat[k] = C.flat[src_idx]
                I_arr.flat[k] = E.flat[src_idx]
                ###print(f"[DEBUG] axis_move(): i_idx={i_idx}, Assigned G.flat[{k}]={G.flat[k]} from C.flat[{src_idx}] "
               #       f"and I_arr.flat[{k}]={I_arr.flat[k]} from E.flat[{src_idx}]")
    
    Cube[AxisFrom - 1] = G
    Cube[AxisTo - 1] = H
    Cube[AxisFrom - 2] = I_arr
    Cube[AxisTo - 2] = J
    """print(f"[DEBUG] axis_move(): Updated Cube faces:\n"
          f"Cube[{AxisFrom - 1}] (G):\n{G}\n"
          f"Cube[{AxisTo - 1}] (H):\n{H}\n"
          f"Cube[{AxisFrom - 2}] (I_arr):\n{I_arr}\n"
          f"Cube[{AxisTo - 2}] (J):\n{J}")
    """
    return Cube


def cube_move(Face, AxisFrom, AxisTo, Slice, Cube, D, s):
    """
    Combines the moves into a single cube move.
    """
    ###print(f"[DEBUG] cube_move() called with Face={Face}, AxisFrom={AxisFrom}, AxisTo={AxisTo}, Slice={Slice}")
    if Slice == 1:
        ###print(f"[DEBUG] cube_move(): Calling face_move() because Slice==1")
        Cube = face_move(Face, AxisFrom, AxisTo, Slice, Cube, D, s)
    ###print(f"[DEBUG] cube_move(): Calling other_move()")
    Cube = other_move(Face, AxisFrom, AxisTo, Slice, Cube, D, s)
    ###print(f"[DEBUG] cube_move(): Calling axis_move()")
    Cube = axis_move(Face, AxisFrom, AxisTo, Slice, Cube, D, s)
    ###print(f"[DEBUG] cube_move(): Move complete, returning Cube")
    return Cube

# -------------------------
# Main Program
# -------------------------

def main():
    print("Welcome to the Higher-Dimensional Rubik's Cube Simulator!")
    # Get the number of dimensions (must be at least 3 lol)
    D = get_int("Enter the number of dimensions (>= 3): ", min_val=3)
    
    # Get the number of slices (divisions per side, at least 2)
    s = get_int("Enter the number of slices or divisions per side (>= 2): ", min_val=2)
    
    iter_val = 1
    # Create the Cube object.
    # Start with a 2D array so that concatenation mimics MATLAB's behavior.
    A = np.array([[1]])
    for i in range(1, D):
        B = A.copy()
        for j in range(1, s):
            A = cat(i, A, B + iter_val)
            iter_val = iter_val + s ** (i - 1)
            ###print(f"[DEBUG] main(): Cube creation loop: i={i}, j={j}, iter_val={iter_val}, A=\n{A}")
    Cube = []
    for k in range(1, 2 * D + 1):
        Cube.append(A + (k - 1) * iter_val)
        ###print(f"[DEBUG] main(): Cube face {k-1} created:\n{Cube[-1]}")
    
    print("\nInitial Cube:")
    for face in Cube:
        print(face)
    
    print("\nCommands:")
    print("  Q - Quit")
    print("  S - Show current state of the Cube")
    print("  M - Make a move")
    
    # Main interactive loop
    while True:
        user_cmd = input("\nEnter command (Q/S/M): ").strip().upper()
        if user_cmd == "Q":
            print("Exiting program.")
            break
        elif user_cmd == "S":
            print("\nCurrent Cube state:")
            for face in Cube:
                print(face)
        elif user_cmd == "M":
            print("\nPlease enter the following move parameters:")
            face = get_int(f"Enter face (1 to {2 * D}): ", min_val=1, max_val=2 * D)
            # Determine the forbidden axes for the chosen face.
            # Faces come in pairs: pair = ceil(face/2). Forbidden axes for that pair:
            pair = (face + 1) // 2  # equivalent to ceil(face/2) for positive integers.
            forbidden = {2 * pair - 1, 2 * pair}
            while True:
                print(f"Info: For face {face}, axis_to cannot be in {forbidden}.")
                axis_from = get_int(f"Enter axis from (1 to {2 * D}): ", min_val=1, max_val=2 * D)
                if axis_from in forbidden:
                    print(f"Error: For face {face}, axis_from cannot be in {forbidden}.")
                else:
                    break
            while True:
                print(f"Info: For face {face}, axis_to cannot be in {forbidden}.")
                axis_to = get_int(f"Enter axis to (1 to {2 * D}): ", min_val=1, max_val=2 * D)
                if axis_to in forbidden:
                    print(f"Error: For face {face}, axis_to cannot be in {forbidden}.")
                else:
                    break
            slice_val = get_int(f"Enter slice (1 to {s}): ", min_val=1, max_val=s)
            try:
                Cube = cube_move(face, axis_from, axis_to, slice_val, Cube, D, s)
                print("Move executed successfully.")
                ###print("[DEBUG] main(): Cube state after move:")
                # for idx, face_array in enumerate(Cube):
                #     print(f"Face {idx}:\n{face_array}")
            except Exception as e:
                print(f"Error during move execution: {e}")
        else:
            print("Invalid command. Please enter Q, S, or M.")

if __name__ == "__main__":
    main()
